import streamlit as st

from services.dynamodb import get_records
from services.s3 import get_image

st.title(
    " Active Alerts"
)

records=[

x

for x

in get_records()

if x["alert"]

]

if not records:

    st.success(
        "No active alerts"
    )

for r in records:

    with st.container():

        c1,c2=st.columns(
            [2,1]
        )

        with c1:

            try:

                img=get_image(
                    r[
                        "processed_image"
                    ]
                )

                st.image(
                    img,
                    use_container_width=True
                )

            except:

                st.error(
                    "Image unavailable"
                )

        with c2:

            st.write(
                f'ID: {r["detection_id"]}'
            )

            st.write(
                r["timestamp"]
            )

            for d in r[
                "detections"
            ]:

                cls=d["class"]

                count=int(
                    d["count"]
                )

                conf=float(
                    d[
                        "max_confidence"
                    ]
                )

                if (
                    cls=="clipping"
                    and
                    count>15
                ):

                    st.error(
                        f"⚠ Critical clipping ({count})"
                    )

                elif cls=="seams":

                    st.warning(
                        f"Seams ({count})"
                    )

                elif cls=="sharp_rails":

                    st.warning(
                        f"Sharp Rails ({count})"
                    )

                else:

                    st.info(
                        f"{cls}: {count}"
                    )

                st.caption(
                    f"Max Confidence: {conf}"
                )

    st.divider()
