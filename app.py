import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# โหลด API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="ระบบตรวจจับรอยแตกร้าว",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 ระบบตรวจจับรอยแตกร้าวในคอนกรีต")
st.write("อัปโหลดรูปภาพโครงสร้าง เพื่อวิเคราะห์รอยแตกร้าวและรับคำแนะนำในการซ่อม")

# อัปโหลดรูป
uploaded_file = st.file_uploader(
    "เลือกรูปภาพ",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="รูปที่อัปโหลด", use_column_width=True)

    if st.button("🔎 วิเคราะห์รอยแตกร้าว"):
        with st.spinner("กำลังวิเคราะห์..."):

            # ส่งรูปให้ Gemini วิเคราะห์
            model = genai.GenerativeModel("gemini-2.5-flash")

            prompt = """
            คุณเป็นวิศวกรโยธาผู้เชี่ยวชาญด้านการตรวจสอบโครงสร้าง
            กรุณาวิเคราะห์รูปภาพนี้และตอบในรูปแบบต่อไปนี้:

            1. **ผลการตรวจจับ**: มีรอยแตกร้าวหรือไม่?
            2. **ประเภทรอยแตก**: (เช่น Hairline Crack, Structural Crack, Shrinkage Crack)
            3. **ความรุนแรง**: (น้อย / ปานกลาง / มาก / วิกฤต)
            4. **สาเหตุที่เป็นไปได้**: 
            5. **คำแนะนำในการซ่อม**: 
            6. **ข้อควรระวัง**: 
            7. **ความเร่งด่วน**: (ซ่อมทันที / ติดตามอย่างใกล้ชิด / ซ่อมตามแผน)

            กรุณาตอบเป็นภาษาไทย
            """

            response = model.generate_content([prompt, image])

            st.success("✅ วิเคราะห์เสร็จแล้ว!")
            st.markdown("### 📋 ผลการวิเคราะห์")
            st.markdown(response.text)
