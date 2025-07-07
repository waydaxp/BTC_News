from fetch_btc_data import get_btc_analysis
import json

btc = get_btc_analysis()
print(json.dumps(btc, indent=2, ensure_ascii=False))
