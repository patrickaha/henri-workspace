import json

data = [
  {
    "date": "20260124",
    "sessions": "12275",
    "conversions": "13942"
  },
  {
    "date": "20260122",
    "sessions": "12081",
    "conversions": "12291"
  },
  {
    "date": "20260120",
    "sessions": "11912",
    "conversions": "12819"
  },
  {
    "date": "20260118",
    "sessions": "11693",
    "conversions": "11702"
  },
  {
    "date": "20260121",
    "sessions": "11037",
    "conversions": "10980"
  },
  {
    "date": "20260114",
    "sessions": "11020",
    "conversions": "11351"
  },
  {
    "date": "20260116",
    "sessions": "11004",
    "conversions": "11775"
  },
  {
    "date": "20260123",
    "sessions": "10843",
    "conversions": "11559"
  },
  {
    "date": "20260113",
    "sessions": "10661",
    "conversions": "10294"
  },
  {
    "date": "20260119",
    "sessions": "10641",
    "conversions": "11302"
  },
  {
    "date": "20260117",
    "sessions": "10411",
    "conversions": "11184"
  },
  {
    "date": "20260115",
    "sessions": "9826",
    "conversions": "10032"
  },
  {
    "date": "20260112",
    "sessions": "8938",
    "conversions": "7924"
  },
  {
    "date": "20260106",
    "sessions": "7749",
    "conversions": "6498"
  },
  {
    "date": "20260105",
    "sessions": "7598",
    "conversions": "5915"
  },
  {
    "date": "20260104",
    "sessions": "7450",
    "conversions": "5694"
  },
  {
    "date": "20260109",
    "sessions": "7197",
    "conversions": "5798"
  },
  {
    "date": "20260103",
    "sessions": "7064",
    "conversions": "5322"
  },
  {
    "date": "20260108",
    "sessions": "7042",
    "conversions": "6005"
  },
  {
    "date": "20260102",
    "sessions": "6872",
    "conversions": "5474"
  },
  {
    "date": "20260107",
    "sessions": "6867",
    "conversions": "6062"
  },
  {
    "date": "20260111",
    "sessions": "6856",
    "conversions": "5584"
  },
  {
    "date": "20251230",
    "sessions": "6730",
    "conversions": "6275"
  },
  {
    "date": "20260101",
    "sessions": "6507",
    "conversions": "5343"
  },
  {
    "date": "20260110",
    "sessions": "6358",
    "conversions": "5507"
  }
]

print("Date       | Sessions | Conversions | Conv Rate | Analysis")
print("--------------------------------------------------------")

# Sort by date
data_sorted = sorted(data, key=lambda x: x['date'])

for item in data_sorted:
    date = item['date']
    sessions = int(item['sessions'])
    conversions = int(item['conversions'])
    conv_rate = (conversions / sessions) * 100
    
    # Determine period
    if date <= "20260112":
        period = "PRE-BATCH"
    else:
        period = "POST-BATCH"
    
    print(f"{date} | {sessions:8} | {conversions:11} | {conv_rate:8.1f}% | {period}")

# Calculate averages
pre_batch = [item for item in data_sorted if item['date'] <= "20260112"]
post_batch = [item for item in data_sorted if item['date'] > "20260112"]

pre_sessions = sum(int(item['sessions']) for item in pre_batch)
pre_conversions = sum(int(item['conversions']) for item in pre_batch)
pre_avg_rate = (pre_conversions / pre_sessions) * 100

post_sessions = sum(int(item['sessions']) for item in post_batch)
post_conversions = sum(int(item['conversions']) for item in post_batch)
post_avg_rate = (post_conversions / post_sessions) * 100

print("\n" + "="*60)
print("SUMMARY ANALYSIS:")
print(f"PRE-BATCH  (≤Jan 12): {pre_avg_rate:.1f}% conversion rate")
print(f"POST-BATCH (>Jan 12): {post_avg_rate:.1f}% conversion rate")
print(f"CHANGE: {post_avg_rate - pre_avg_rate:+.1f} percentage points")
print("="*60)