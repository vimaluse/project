import csv

INPUT_FILE = "inventory.csv"
OUTPUT_FILE = "restock_report.csv"

restock_items = []

with open(INPUT_FILE, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        current_stock = int(row["Current_Stock"])
        reorder_level = int(row["Reorder_Level"])

        if current_stock < reorder_level:

          
            if current_stock <= (0.25 * reorder_level):
                priority = "Critical"
            else:
                priority = "Low"
              
            healthy_stock = reorder_level * 2
            quantity_to_order = healthy_stock - current_stock

            restock_items.append({
                "Item_ID": row["Item_ID"],
                "Item_Name": row["Item_Name"],
                "Category": row["Category"],
                "Current_Stock": current_stock,
                "Reorder_Level": reorder_level,
                "Priority": priority,
                "Supplier": row["Supplier"],
                "Suggested_Reorder": quantity_to_order
            })

with open(OUTPUT_FILE, "w", newline="") as file:

    fieldnames = [
        "Item_ID",
        "Item_Name",
        "Category",
        "Current_Stock",
        "Reorder_Level",
        "Priority",
        "Supplier",
        "Suggested_Reorder"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(restock_items)


print("=" * 75)
print("                INVENTORY REORDER REPORT")
print("=" * 75)

if restock_items:

    for item in restock_items:
        print(
            f"{item['Item_Name']:<15}"
            f"Stock: {item['Current_Stock']:<5}"
            f"Threshold: {item['Reorder_Level']:<5}"
            f"Priority: {item['Priority']:<10}"
            f"Order Qty: {item['Suggested_Reorder']}"
        )

else:
    print("All inventory levels are healthy.")


print("\n")
print("=" * 75)
print("SIMULATED EMAIL ALERT")
print("=" * 75)

print("Subject: Inventory Restock Alert")

print("\nDear Warehouse Manager,\n")

if restock_items:

    print("The following inventory items require immediate attention:\n")

    for item in restock_items:
        print(
            f"- {item['Item_Name']} "
            f"(Current Stock: {item['Current_Stock']}, "
            f"Threshold: {item['Reorder_Level']}, "
            f"Priority: {item['Priority']}, "
            f"Suggested Order: {item['Suggested_Reorder']} units)"
        )

    print("\nPlease place purchase orders with the respective suppliers.")

else:
    print("No items require restocking today.")

print("\nRegards")
print("Inventory Monitoring System")

print("\nCSV Report Generated Successfully:", OUTPUT_FILE)

print("\nReflection Note")
print("-" * 40)
print("1. Schedule this script to run automatically every day using Task Scheduler or Cron.")
print("2. Integrate supplier APIs to automatically place purchase orders.")
print("3. Track historical inventory trends to forecast future demand.")
print("4. Add email sending using Python's smtplib instead of printing the email.")
print("5. Store inventory in a database instead of CSV for better scalability.")
