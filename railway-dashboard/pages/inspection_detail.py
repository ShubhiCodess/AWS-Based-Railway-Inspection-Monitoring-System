import streamlit as st

from services.dynamodb import get_records
from services.s3 import get_image

st.title(
"Inspection Detail"
)

records=get_records()

ids=[

x[
"detection_id"
]

for x

in records
]

selected=st.selectbox(

"Select Inspection",

ids
)

record=[

x

for x

in records

if

x[
"detection_id"
]

==
selected

][0]

img=get_image(

record[
"processed_image"
]
)

st.image(

img,

use_container_width=True
)

st.subheader(
"Detections"
)

for d in record[
"detections"
]:

    st.metric(

        d[
            "class"
        ],

        d[
            "count"
        ],

        float(
            d[
                "max_confidence"
            ]
        )
    )

if (
record[
"latitude"
]
is None
):

    st.warning(
"Location unavailable"
)

else:

    st.success(

f'''
Lat:
{record["latitude"]}

Lon:
{record["longitude"]}
'''
)

