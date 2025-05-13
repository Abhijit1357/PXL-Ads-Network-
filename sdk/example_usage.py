from fetch_ad import get_ad

def send_message_with_ad(user_id, bot_id, send_func):
    ad_text = get_ad(bot_id)
    if ad_text:
        send_func(user_id, ad_text)

# Example send function
def dummy_send(user_id, text):
    print(f"Sending to {user_id}: {text}")

# Test
if __name__ == "__main__":
    send_message_with_ad(123456, "my_test_bot", dummy_send)
