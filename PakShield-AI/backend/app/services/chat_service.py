from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.chat import ChatMessage

PAKISTAN_CURRENCY_KEYWORDS = [
    "pakistan", "rupee", "pkr", "currency", "banknote", "note", "fake", "real",
    "counterfeit", "genuine", "detect", "scan", "5000", "1000", "100", "50",
    "jinnah", "watermark", "security thread", "serial number", "denomination",
    "state bank", "sbp", "pakistani", "money", "bill", "notes",
]


def _is_currency_related(message: str) -> bool:
    msg_lower = message.lower()
    for kw in PAKISTAN_CURRENCY_KEYWORDS:
        if kw in msg_lower:
            return True
    return False


def _generate_chatbot_reply(message: str) -> str:
    msg = message.lower()

    if not _is_currency_related(message):
        return (
            "I can only answer questions about Pakistani currency. "
            "Please ask about Pakistani banknotes, fake note detection, "
            "currency security features, or related topics."
        )

    if "hello" in msg or "hi" in msg or "assalam" in msg:
        return "Assalam-o-Alaikum! I am PakShield AI. I can help you detect fake Pakistani currency notes. Upload an image or ask me anything about Pakistani rupees."

    if any(w in msg for w in ["fake", "counterfeit", "real", "genuine", "detect"]):
        if "how" in msg:
            return (
                "PakShield AI uses deep learning (EfficientNetB0) to analyze "
                "banknote images. It checks watermark integrity, microtext clarity, "
                "serial number patterns, and ink fluorescence to determine authenticity. "
                "Upload a clear image of the note for analysis."
            )
        return (
            "To detect fake Pakistani currency:\n"
            "1. Upload a clear image of the banknote (front side preferred)\n"
            "2. Our AI analyzes watermark, security thread, microtext, and serial number\n"
            "3. Results show REAL or FAKE with confidence score\n"
            "4. Check security features: watermark of Jinnah, security thread, raised printing, UV features"
        )

    if "security" in msg and ("feature" in msg or "element" in msg):
        return (
            "Key security features of Pakistani currency notes:\n"
            "• Watermark: Quaid-e-Azam Mohammad Ali Jinnah's portrait\n"
            "• Security thread: Color-changing thread with text\n"
            "• Microtext: Very small text visible under magnification\n"
            "• Raised printing: Intaglio print on specific areas\n"
            "• UV features: Fluorescent elements visible under UV light\n"
            "• Serial numbers: Unique number combination\n"
            "• See-through register: Design elements that align when held to light"
        )

    if any(w in msg for w in ["5000", "5000 rupee", "5000 note"]):
        return (
            "The PKR 5000 note is Pakistan's highest denomination. Key features:\n"
            "• Color: Dark green/mustard\n"
            "• Front: Quaid-e-Azam M.A. Jinnah\n"
            "• Back: Islamabad's Faisal Mosque\n"
            "• Security thread: Green color-shifting thread\n"
            "• Watermark: Jinnah portrait with 5000\n"
            "• Issued: 2006 (series started)\n"
            "Always check the security thread and watermark for authenticity."
        )

    if any(w in msg for w in ["1000", "1000 rupee", "1000 note"]):
        return (
            "The PKR 1000 note features:\n"
            "• Color: Dark blue/purple\n"
            "• Front: Quaid-e-Azam M.A. Jinnah\n"
            "• Back: Islamia College Peshawar\n"
            "• Security thread: Green with shifting color\n"
            "• Watermark: Jinnah portrait with 1000\n"
            "Look for the security thread and microtext to verify authenticity."
        )

    if "100 rupee" in msg or "100 note" in msg:
        return (
            "The PKR 100 note features:\n"
            "• Color: Red/Green\n"
            "• Front: Quaid-e-Azam M.A. Jinnah\n"
            "• Back: Quaid-e-Azam Residency, Ziarat\n"
            "• Security thread: Metallic thread\n"
            "• Watermark: Jinnah portrait\n"
            "Commonly counterfeited, always check the watermark."
        )

    if "timeline" in msg or "history" in msg:
        return (
            "Pakistani Currency Timeline:\n"
            "1947: Pakistan adopted Indian Rupee with overprints\n"
            "1948: First Pakistani coins issued\n"
            "1949: First Pakistan Rupee notes issued (1, 5, 10, 100)\n"
            "1986: 50 Rupee note introduced\n"
            "1997: 5000 Rupee note introduced\n"
            "2006: New series with enhanced security features launched\n"
            "2022: Revised notes with updated security features\n"
            "2024: Ongoing modernization of currency design"
        )

    if "rate" in msg or "exchange" in msg or "ticker" in msg:
        return (
            "PakShield AI provides live PKR exchange rates on the dashboard. "
            "Current approximate rates (check dashboard for live):\n"
            "USD/PKR, EUR/PKR, GBP/PKR, AED/PKR, SAR/PKR, CNY/PKR"
        )

    return (
        "I specialize in Pakistani currency detection and information. "
        "You can ask me about:\n"
        "• Detecting fake vs real banknotes\n"
        "• Security features of Pakistani currency\n"
        "• PKR note denominations (100, 1000, 5000)\n"
        "• Currency history and timeline\n"
        "• Exchange rates\n"
        "Or upload a note image for AI analysis!"
    )


async def process_chat_message(
    db: AsyncSession,
    user_id: str,
    message: str,
) -> tuple[str, str]:
    user_msg = ChatMessage(user_id=user_id, role="user", content=message)
    db.add(user_msg)

    reply_text = _generate_chatbot_reply(message)

    bot_msg = ChatMessage(user_id=user_id, role="assistant", content=reply_text)
    db.add(bot_msg)
    await db.commit()
    await db.refresh(bot_msg)

    return reply_text, bot_msg.id
