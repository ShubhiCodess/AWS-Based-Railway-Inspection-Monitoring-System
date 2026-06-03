import streamlit as st
import pandas as pd

from services.dynamodb import get_records

records=get_records()

total=len(records)

alerts=sum(
1
for x
in records
if x["alert"]
)

defects=0

for r in records:

    for d in r["detections"]:

        defects+=d["count"]

c1,c2,c3,c4=st.columns(4)

c1.metric(
"Inspections",
total
)

c2.metric(
"Alerts",
alerts
)

c3.metric(
"Images",
total
)

c4.metric(
"Defects",
defects
)

st.divider()

df=[]

for r in records:

    for d in r[
        "detections"
    ]:

        df.append({

            "class":
            d["class"],

            "count":
            d["count"]
        })

if df:

    df=pd.DataFrame(
        df
    )

    st.bar_chart(

        df.groupby(
            "class"
        )[
            "count"
        ]
        .sum()
    )

