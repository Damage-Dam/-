from flask import Flask, request, jsonify
from datetime import datetime
import csv

app = Flask(__name__)


# 读取CSV数据
def read_sales_data(csv_file_path):
    sales_data = []
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sales_data.append({
                "date": row["日期"],
                "product": row["产品名称"],
                "quantity": int(row["销售数量"]),
                "unit_price": float(row["单价"]),
                "total_sales": float(row["销售金额"])
            })
    return sales_data


sales_data = read_sales_data('sales_data.csv')


# 获取销售趋势数据
@app.route('/api/sales/trends', methods=['GET'])
def get_sales_trends():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"status": "error", "message": "start_date and end_date are required"}), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date format"}), 400

    trend_data = [
        {"date": entry["date"], "sales": entry["total_sales"]}
        for entry in sales_data
        if start_date <= datetime.strptime(entry["date"], '%Y-%m-%d') <= end_date
    ]

    return jsonify({"status": "success", "data": trend_data})


# 获取各地区销售对比数据
@app.route('/api/sales/region-comparison', methods=['GET'])
def get_region_comparison():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"status": "error", "message": "start_date and end_date are required"}), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date format"}), 400

    region_sales = {}
    for entry in sales_data:
        entry_date = datetime.strptime(entry["date"], '%Y-%m-%d')
        if start_date <= entry_date <= end_date:
            region = entry["product"]
            sales = entry["total_sales"]
            if region in region_sales:
                region_sales[region] += sales
            else:
                region_sales[region] = sales

    comparison_data = [{"region": region, "sales": sales} for region, sales in region_sales.items()]

    return jsonify({"status": "success", "data": comparison_data})


# http://127.0.0.1:5000/api/sales/trends
# http://127.0.0.1:5000/api/sales/region-comparison
if __name__ == '__main__':
    app.run(debug=True)
