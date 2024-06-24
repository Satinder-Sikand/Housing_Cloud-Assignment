import pandas as pd

def print_full(x):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')

# Base url
base_url = "C:\\Users\\HP\\Downloads\\analytics_eng_interview\\anaytics_eng_interview\\"
pd.set_option('display.max_columns', None)
# Define file paths
persons_data_path = base_url+ "persons_data.csv"
occupancy_data_path = base_url+ "occupancy_data.csv"
majors_data_path = base_url+ "majors_data.csv"
inventory_data_path = base_url+ "inventory_data.csv"
output_file_path = base_url+ "combined_data.csv"

# Read majors in
majors: pd.DataFrame = pd.read_csv(majors_data_path)
majors = majors.groupby('name').agg(count = ("name", "count"), id=('id', 'first')) # Count number o each major name group
print_full(majors.head(1))
print(f'major#: {majors.shape[0]}')
# commonid2 = majors[majors["displayId"].isin(majors["id"])]["displayId"].unique()
# print_full(commonid2)

# Read persons in
persons: pd.DataFrame = pd.read_csv(persons_data_path)

# Convert the addresses
def convert(split):
    split = split.split(",")
    if len(split)==3:
        split.insert(1, ' ')
    elif len(split)==4:
        split.append(' ')
        return split
    else:
        split = [' ', ' ', ' ', ' ']
    split.append(' ')
    return split

# Add name row, populate by first name + last name
persons["name"] = persons.apply(lambda row: row['firstName'] + ' ' + row['lastName'], axis='columns', result_type='expand')
# Add address information by splitting address
persons[['address1', 'address2', 'city', 'state', 'zip']] = persons.apply(lambda row: convert(row['address']), axis='columns', result_type='expand')
#Remove persons without an major, keep original copy
original_persons = persons.copy()
print(f'Check # of unique emails: {persons.drop_duplicates(subset="email", keep="first").shape[0]}' ) #See unique emails
print(f'People# before throwing out null majors: {persons.shape[0]}')

# Check amount of each email now
# temp= persons.groupby('email').agg(count = ("email", "count"))
# temp = temp.agg(total = ("count", "count"))
# print(temp.head(2))

print_full(persons.head(5))

# Read in the occupancy and inventory csvs
occupancy = pd.read_csv(occupancy_data_path).groupby(["buildingName", "roomName", "bedName"]).agg(personId = ("personId", "first"))

inventory = pd.read_csv(inventory_data_path).groupby(["buildingName", "roomName", "bedName"]).agg(bedId = ("bedId", "first"))
# print(occupancy.shape[0])
# print(inventory.shape[0])

# Create a join of the inventory/bed occupation table and the bedId table
personToBedId = occupancy.join(inventory, on=["buildingName", "roomName", "bedName"], how='inner').reset_index()[["personId", "bedId"]]
print("\n\n")
print(personToBedId.columns)
# personToBedId = personToBedId.drop(columns=["buildingName", "roomName", "bedName"])
print_full(personToBedId.head(2))
print(personToBedId.shape[0])

# Join the bedIds based off of the personId
persons = persons.join(personToBedId.set_index("personId"), on="personId", how="left")
# Replace major text with major id's
majors = majors["id"]
print_full(majors.head(1))
print(f'major#: {majors.shape[0]}')
def majorTextToId(majorText):
    if not majorText or majorText!=majorText:
        return None
    majorText = majorText.split(',')
    idMajors = []
    for m in majorText:
        m = m.strip()
        m = majors.get(m, None)
        if m:
            idMajors.append(m )

        # idMajors.append(majors[majors["name"].str.strip().str.lower()==m.lower()]["id"].get(0))
    return ', '.join(idMajors)

# Change every majors to majorIds
persons['majors'] = persons.apply(lambda row: majorTextToId(row['majors']), axis='columns')
# Rename all columns as needed and cut off unneeded columns
persons = persons.rename(columns={"majors": "majorIds"})[["personId", "name", "email", "dob", "address1", "address2", "city", "state", "zip", "majorIds", "bedId"]].set_index("personId")
persons['bedId'] = persons.apply(lambda row: None if row['bedId']!=row['bedId'] or row['bedId'] is None else row['bedId'], axis='columns' )
# Filter for only valid copies now, but keep original copy of people
original_persons = persons.copy()
# Remove any person that doesn't have a majorId or a bedId
persons = persons[(~persons['majorIds'].isnull()) & (~persons['bedId'].isnull())]
print(f'Total number of nearly valid: {persons.shape[0]}')
# Keep only first copy of person email
persons = persons.drop_duplicates(subset="email")

print_full(persons.head(5))
print(persons.shape[0])

original_persons = pd.concat([original_persons, persons]).drop_duplicates(keep=False)

print_full(original_persons.head(5))
print(original_persons.shape[0])

# Write to files
persons.to_csv(base_url+"included_answer.csv")
original_persons.to_csv(base_url+"removed_answer.csv")