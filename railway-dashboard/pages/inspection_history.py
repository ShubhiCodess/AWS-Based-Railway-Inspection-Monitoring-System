import streamlit as st

from services.dynamodb import get_records
from services.transforms import flatten

st.title(
"Inspection History"
)

records=get_records()

df=flatten(
records
)

search=st.text_input(
"Search"
)

if search:

    df=df[
        df.astype(
            str
        )
        .apply(
            lambda x:
            x.str.contains(
                search,
                case=False
            )
        )
        .any(1)
    ]

alert_filter=st.selectbox(

"Alert",

[
"All",
True,
False
]
)

if alert_filter!="All":

    df=df[
        df.alert==
        alert_filter
    ]

st.dataframe(

df,

use_container_width=True
)
