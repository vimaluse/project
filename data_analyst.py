import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("funnel_events_sample (1).csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])

df = df.drop_duplicates(subset=["user_id", "step"])

steps = [
    "visited_site",
    "signup_started",
    "details_filled",
    "email_verified",
    "purchase_completed"
]

funnel_data = []

previous_count = None

for step in steps:
    count = df[df["step"] == step]["user_id"].nunique()

    if previous_count is None:
        conversion = 100.0
    else:
        conversion = round((count / previous_count) * 100, 2)

    dropoff = 100 - conversion

    funnel_data.append({
        "Step": step,
        "Users": count,
        "Conversion Rate (%)": conversion,
        "Drop-off (%)": round(dropoff, 2)
    })

    previous_count = count

funnel_report = pd.DataFrame(funnel_data)

print("\n==============================")
print("FUNNEL ANALYSIS")
print("==============================")
print(funnel_report)


drop_df = funnel_report.iloc[1:]

worst = drop_df.loc[drop_df["Drop-off (%)"].idxmax()]

print("\n==============================")
print("BIGGEST DROP-OFF")
print("==============================")
print(f"Stage : {worst['Step']}")
print(f"Drop-off : {worst['Drop-off (%)']}%")


funnel_report.to_csv("funnel_report.csv", index=False)

print("\nReport exported as funnel_report.csv")

plt.figure(figsize=(8,5))

plt.bar(
    funnel_report["Step"],
    funnel_report["Users"]
)

plt.title("Funnel Analysis")
plt.xlabel("Funnel Stage")
plt.ylabel("Unique Users")
plt.xticks(rotation=20)

plt.tight_layout()
plt.show()


print("\n==============================")
print("AVERAGE TIME TO CONVERT")
print("==============================")

for i in range(len(steps)-1):

    first = steps[i]
    second = steps[i+1]

    first_df = df[df["step"] == first][["user_id","timestamp"]]
    second_df = df[df["step"] == second][["user_id","timestamp"]]

    merged = pd.merge(
        first_df,
        second_df,
        on="user_id",
        suffixes=("_1","_2")
    )

    if len(merged) > 0:

        merged["minutes"] = (
            merged["timestamp_2"] -
            merged["timestamp_1"]
        ).dt.total_seconds()/60

        avg = round(merged["minutes"].mean(),2)

        print(f"{first} --> {second} : {avg} minutes")


df["Segment"] = df["user_id"].apply(
    lambda x:
    "Even"
    if int(x[1:]) % 2 == 0
    else "Odd"
)

print("\n==============================")
print("SEGMENT COMPARISON")
print("==============================")

segment_table = pd.pivot_table(
    df,
    values="user_id",
    index="Segment",
    columns="step",
    aggfunc="nunique"
)

print(segment_table)

print("\n==============================")
print("RECOMMENDATION")
print("==============================")

print(
"""
The largest user drop-off occurs at the stage shown above.
This suggests users experience friction before progressing further.
Improve this step by simplifying the form, reducing required fields,
or improving page performance and error handling.
Running A/B tests on this stage can help improve conversion rates.
"""
)
