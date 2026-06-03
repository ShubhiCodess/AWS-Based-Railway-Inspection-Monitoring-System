import streamlit as st
import pandas as pd
import plotly.express as px

from services.dynamodb import get_records

st.title(
"Analytics"
)

records=get_records()

rows=[]

for r in records:

    total=0

    for d in r[
        "detections"
    ]:

        total+=int(
            d["count"]
        )

        rows.append({

            "timestamp":
            r[
                "timestamp"
            ],

            "class":
            d[
                "class"
            ],

            "count":
            int(
                d[
                    "count"
                ]
            )
        })

df=pd.DataFrame(
    rows
)

total_images=len(
    records
)

avg=df[
    "count"
].mean()

common=df.groupby(
    "class"
)[
    "count"
].sum().idxmax()

c1,c2,c3=st.columns(
3
)

c1.metric(
"Total Images",
total_images
)

c2.metric(
"Avg/Image",
round(avg,2)
)

c3.metric(
"Most Common",
common
)

st.subheader(
"Trend"
)

trend=df.groupby(
[
"timestamp",
"class"
]
)[
"count"
].sum()

trend=trend.reset_index()

fig=px.line(

trend,

x=
"timestamp",

y=
"count",

color=
"class"
)

st.plotly_chart(
fig,
use_container_width=True
)

st.subheader(
"Distribution"
)

fig2=px.histogram(

df,

x=
"class",

y=
"count"
)

st.plotly_chart(
fig2,
use_container_width=True
)
