from flask import make_response
from io import StringIO
import csv


def dl_general():
    file = StringIO()
    writer = csv.writer(file, lineterminator="\n")
    writer.writerow(
            ['注文番号', '登録日', '営業担当', '顧客ID', '事業所ID', '事業所名', '都道府県', '商品番号', '商品名', '単価', '数量']
        )

    response = make_response()
    response.data = file.getvalue().encode('sjis', 'replace')
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=orders-' + 'target' + '.csv'
    
    return response
