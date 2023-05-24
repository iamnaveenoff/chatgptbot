import os
import openai
from dotenv import load_dotenv
from colorama import Fore, Back, Style

# load values from the .env file if it exists
load_dotenv()

# configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

INSTRUCTIONS = """<<PUT THE PROMPT HERE>>"""

TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 10


def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return completion.choices[0].message.content


def get_moderation(question):
    """
    Check if the question is safe to ask the model

    Parameters:
        question (str): The question to check

    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        # get the categories that are flagged and generate a message
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None


def main():
    os.system("cls" if os.name == "nt" else "clear")
    # keep track of previous questions and answers
    previous_questions_and_answers = []

    # Define user-defined questions and answers
    user_data = [
    {
        "question": "What are your shipping options?",
        "answer": "We offer various shipping options including standard ground shipping, express shipping, and overnight shipping."
    },
    {
        "question": "How can I track my shipment?",
        "answer": "You can track your shipment by entering the tracking number provided in the shipping confirmation email on our website's tracking page."
    },
    {
        "question": "What is the estimated delivery time for standard shipping?",
        "answer": "The estimated delivery time for standard shipping is typically 3-5 business days, but it may vary depending on the destination."
    },
    {
        "question": "What should I do if my package is damaged during transit?",
        "answer": "If your package arrives damaged, please contact our customer service immediately with photos of the damaged package and item, and we will assist you with the necessary steps."
    },
    {
        "question": "Can I change the shipping address after placing an order?",
        "answer": "We can update the shipping address if the order has not been shipped yet. Please contact our customer service as soon as possible to request the change."
    },
    {
        "question": "What is your return policy for damaged or defective items?",
        "answer": "If you receive a damaged or defective item, please contact our customer service within 48 hours of delivery, and we will arrange for a return or replacement."
    },
    {
        "question": "Do you offer international shipping?",
        "answer": "Yes, we offer international shipping to select countries. Please check our website or contact our customer service for more information on international shipping options."
    },
    {
        "question": "How can I get a shipping quote for international shipments?",
        "answer": "To obtain a shipping quote for international shipments, please provide the destination country, package weight and dimensions, and contact our customer service."
    },
    {
        "question": "What should I do if my package is lost?",
        "answer": "If your package is lost in transit, please contact our customer service, and we will initiate an investigation with the shipping carrier to locate your package or provide a refund."
    },
    {
        "question": "Can I cancel my order before it is shipped?",
        "answer": "Yes, you can cancel your order before it is shipped. Please contact our customer service as soon as possible with your order details to request the cancellation."
    },
    {
        "question": "What forms of payment do you accept?",
        "answer": "We accept major credit cards, debit cards, and PayPal as forms of payment for online orders."
    },
    {
        "question": "How can I request a refund?",
        "answer": "To request a refund, please contact our customer service with your order details and reason for the refund, and we will assist you with the refund process."
    },
    {
        "question": "What is the process for filing a shipping insurance claim?",
        "answer": "If you purchased shipping insurance, and your package is lost or damaged, please contact our customer service, and we will guide you through the process of filing a shipping insurance claim."
    },
    {
        "question": "Do you offer expedited shipping for urgent orders?",
        "answer": "Yes, we offer expedited shipping options for urgent orders. During the checkout process, you can select the desired expedited shipping method."
    },
    {
        "question": "Can I request a specific delivery date for my order?",
        "answer": "While we cannot guarantee a specific delivery date, you can leave a note during the checkout process with your preferred delivery date, and we will do our best to accommodate it."
    },
    {
        "question": "How can I contact your customer service?",
        "answer": "You can contact our customer service by phone at +1-123-456-7890 or by email at support@logisticscompany.com. We are available to assist you during our business hours."
    },
    {
        "question": "What are your customer service hours?",
        "answer": "Our customer service is available from Monday to Friday, 9:00 AM to 5:00 PM (local time)."
    },
    {
        "question": "Do you offer live chat support?",
        "answer": "Yes, we offer live chat support on our website during our customer service hours. Look for the chat icon on our website to start a live chat with our support team."
    },
    {
        "question": "How long does it take to receive a response from customer service?",
        "answer": "We strive to respond to customer inquiries within 24 hours. However, during peak times, it may take slightly longer. We appreciate your patience."
    },
    {
        "question": "What information do I need to provide when contacting customer service?",
        "answer": "When contacting customer service, please provide your order number, the email address associated with your account, and a detailed description of your inquiry or issue."
    },
    {
        "question": "Can I request a change to my order after it has been placed?",
        "answer": "If you need to make changes to your order, such as adding or removing items, please contact our customer service as soon as possible, and we will check if the changes can be accommodated."
    },
    {
        "question": "What should I do if I receive the wrong item?",
        "answer": "If you receive the wrong item, please contact our customer service immediately with your order details and a description of the incorrect item, and we will arrange for a return or replacement."
    },
    {
        "question": "Are there any additional fees or customs duties for international shipments?",
        "answer": "Additional fees or customs duties may apply for international shipments depending on the destination country's regulations. Please check with your local customs office for more information."
    },
    {
        "question": "How can I provide feedback about my customer service experience?",
        "answer": "We value your feedback. You can provide feedback about your customer service experience by contacting our customer service or by filling out the feedback form on our website."
    },
    {
        "question": "What should I do if my package is marked as delivered but I haven't received it?",
        "answer": "If your package is marked as delivered but you haven't received it, please check with your neighbors or building management to ensure it wasn't left with them. If you still can't locate the package, contact our customer service for further assistance."
    },
    {
        "question": "Do you offer order tracking notifications?",
        "answer": "Yes, we provide order tracking notifications via email or SMS. During the checkout process, you can choose your preferred notification method."
    },
    {
        "question": "Can I change the shipping method after placing an order?",
        "answer": "If your order has not been shipped yet, we may be able to change the shipping method. Please contact our customer service as soon as possible to request the change."
    },
    {
        "question": "What should I do if my package is delayed?",
        "answer": "If your package is delayed beyond the estimated delivery time, please contact our customer service, and we will investigate the issue and provide you with an update."
    },
    {
        "question": "Do you offer bulk shipping discounts?",
        "answer": "Yes, we offer bulk shipping discounts for large orders. Please contact our customer service or sales team for more information on bulk shipping rates."
    },
    {
        "question": "What is your policy for missing items in a shipment?",
        "answer": "If there are missing items in your shipment, please contact our customer service with your order details and a description of the missing items, and we will assist you in resolving the issue."
    },
    {
        "question": "Can I request a signature upon delivery for my package?",
        "answer": "Yes, you can request a signature upon delivery for your package during the checkout process. There may be additional charges for this service."
    },
    {
        "question": "How can I provide feedback about the quality of your products?",
        "answer": "We appreciate your feedback about the quality of our products. You can provide feedback by leaving a review on our website or contacting our customer service directly."
    },
    {
        "question": "Do you offer expedited customs clearance for international shipments?",
        "answer": "While we cannot expedite customs clearance, we ensure all necessary customs documentation is provided accurately to minimize any delays in the customs clearance process."
    },
    {
        "question": "What should I do if I receive a damaged package but the contents are unaffected?",
        "answer": "If you receive a damaged package but the contents are unaffected, please contact our customer service and provide photos of the damaged package. We will assess the situation and assist you accordingly."
    },
    {
        "question": "Can I schedule a specific delivery time for my order?",
        "answer": "Unfortunately, we cannot guarantee specific delivery times. Delivery times may vary depending on the shipping carrier and the destination. However, you can track your shipment to get an estimated delivery window."
    },
    {
        "question": "What is your policy for late deliveries?",
        "answer": "We strive to deliver orders on time, and most deliveries are completed within the estimated timeframe. If your order is significantly delayed, please contact our customer service, and we will investigate the issue."
    },
    {
        "question": "Can I ship to a PO Box address?",
        "answer": "In most cases, we can ship to PO Box addresses. However, certain shipping carriers or destinations may have restrictions. Please check with our customer service to confirm if PO Box delivery is available for your order."
    },
    {
        "question": "What should I do if I receive a defective product?",
        "answer": "If you receive a defective product, please contact our customer service within the designated warranty period. We will guide you through the return and replacement process."
    },
    {
        "question": "Can I request a specific carrier for my shipment?",
        "answer": "In general, we determine the shipping carrier based on factors such as the destination, package weight, and service availability. However, you can contact our customer service to inquire about the possibility of using a specific carrier for your shipment."
    },
    {
        "question": "What is your policy for order cancellations?",
        "answer": "You can cancel your order before it is shipped. Please contact our customer service as soon as possible with your order details to request the cancellation. If the order has already been shipped, you may need to initiate a return or follow our return policy."
    },
    {
        "question": "How can I provide feedback about your customer service?",
        "answer": "We appreciate your feedback about our customer service. You can provide feedback by leaving a review on our website or contacting our customer service department directly."
    },
    {
        "question": "Can I request special packaging for fragile items?",
        "answer": "If you have specific packaging requirements for fragile items, please contact our customer service before placing your order. We will do our best to accommodate your request."
    },
    {
        "question": "What should I do if my package is stolen?",
        "answer": "If your package is stolen after being marked as delivered, please contact our customer service and file a report with your local law enforcement agency. We will assist you to the best of our ability."
    },
    {
        "question": "Do you offer weekend delivery options?",
        "answer": "We offer weekend delivery options in select areas. During the checkout process, you can check the availability of weekend delivery for your specific location."
    },
    {
        "question": "Can I change the delivery address after the package has been shipped?",
        "answer": "Once the package has been shipped, it is challenging to change the delivery address. However, you can contact the shipping carrier directly and inquire about any possible options."
    },
    {
        "question": "What should I do if I receive an incorrect invoice?",
        "answer": "If you receive an incorrect invoice, please contact our customer service with the invoice details, and we will rectify the issue as soon as possible."
    },
    {
        "question": "What are your shipping restrictions for hazardous materials?",
        "answer": "We comply with shipping regulations regarding hazardous materials. Certain hazardous materials may be restricted or require additional documentation. Please contact our customer service for guidance on shipping hazardous materials."
    },
    {
        "question": "How can I request a copy of my shipping receipt?",
        "answer": "To request a copy of your shipping receipt, please contact our customer service with your order details, and we will provide you with the necessary documentation."
    },
    {
        "question": "Can I change the shipping method for an existing order?",
        "answer": "If your order has not been shipped yet, we may be able to change the shipping method. Please contact our customer service as soon as possible to request the change."
    },
    {
        "question": "What should I do if my package is returned to sender?",
        "answer": "If your package is returned to us as undeliverable, please contact our customer service with your order details, and we will assist you in reshipping the package to the correct address."
    },
    {
        "question": "Do you offer expedited international shipping?",
        "answer": "Yes, we offer expedited international shipping options for faster delivery. During the checkout process, you can select the desired expedited shipping method for international orders."
    },
    {
        "question": "Can I change the recipient's name on the shipping label?",
        "answer": "To change the recipient's name on the shipping label, please contact our customer service as soon as possible. We will assess the situation and assist you accordingly."
    },
    {
        "question": "What should I do if my package is stuck in customs?",
        "answer": "If your package is stuck in customs, it is typically awaiting clearance by the customs authorities. Please allow some time for the clearance process. If there are any issues, our customer service will assist you in resolving them."
    },
    {
        "question": "Can I request a specific delivery window for my order?",
        "answer": "While we cannot guarantee a specific delivery window, you can track your shipment to get an estimated delivery window. Some shipping carriers may offer delivery notifications or options to reschedule delivery."
    },
    {
        "question": "How can I check the status of my order?",
        "answer": "You can check the status of your order by logging into your account on our website and viewing the order details. Alternatively, you can contact our customer service with your order number for an update."
    },
    {
        "question": "Do you offer free shipping?",
        "answer": "We may offer free shipping for orders that meet specific criteria, such as a minimum order value or during promotional periods. Please check our website or contact our customer service for information on current free shipping offers."
    },
    {
        "question": "What should I do if I receive an incomplete order?",
        "answer": "If you receive an incomplete order, please contact our customer service immediately with your order details and a description of the missing items. We will investigate the issue and rectify it as soon as possible."
    },
    {
        "question": "Do you provide shipping labels for returns?",
        "answer": "Yes, we provide shipping labels for returns. Please contact our customer service with your return request, and we will provide you with a shipping label to return the item."
    },
    {
        "question": "What should I do if my package is marked as delivered but I can't find it?",
        "answer": "If your package is marked as delivered but you can't find it, please check with your neighbors or building management to ensure it wasn't left with them. If you still can't locate the package, contact our customer service for further assistance."
    },
    {
        "question": "Can I request a specific carrier for international shipments?",
        "answer": "We work with various shipping carriers for international shipments based on factors such as the destination, service availability, and efficiency. We cannot guarantee a specific carrier for international shipments."
    },
    {
        "question": "What should I do if my package is delivered to the wrong address?",
        "answer": "If your package is delivered to the wrong address, please contact our customer service immediately. We will initiate an investigation with the shipping carrier and work towards resolving the issue."
    },
    {
        "question": "Do you offer insurance for shipments?",
        "answer": "Yes, we offer shipping insurance for added protection. During the checkout process, you can select the option to purchase shipping insurance for your order."
    },
    {
        "question": "Can I request a refund for shipping charges if my package is delayed?",
        "answer": "Shipping charges are generally non-refundable, even if there is a delay in the delivery. Please refer to our shipping policy for more information or contact our customer service for assistance."
    },
    {
        "question": "What should I do if I receive a package that isn't mine?",
        "answer": "If you receive a package that isn't yours, please contact our customer service immediately with details of the incorrect delivery. We will arrange for the retrieval of the package and ensure the correct one reaches you."
    },
    {
        "question": "Can I request a specific shipping carrier for my order?",
        "answer": "While we cannot guarantee a specific shipping carrier, you can leave a note during the checkout process with your preferred carrier, and we will do our best to accommodate it."
    },
    {
        "question": "How can I request a delivery confirmation for my package?",
        "answer": "You can request a delivery confirmation for your package by selecting the appropriate option during the checkout process. Delivery confirmation may be available for certain shipping methods or at an additional cost."
    },
    {
        "question": "What should I do if my package is delayed due to weather conditions?",
        "answer": "If your package is delayed due to weather conditions, please be patient as it is beyond our control. We will work with the shipping carrier to ensure your package is delivered as soon as it is safe to do so."
    },
    {
        "question": "Do you offer local pickup options?",
        "answer": "Yes, we offer local pickup options for customers in select areas. During the checkout process, you can check if local pickup is available for your location."
    },
    {
        "question": "Can I change the delivery address after placing an order?",
        "answer": "If your order has not been shipped yet, we may be able to change the delivery address. Please contact our customer service as soon as possible to request the change."
    },
    {
        "question": "What should I do if my package is lost during transit?",
        "answer": "If your package is lost during transit, please contact our customer service immediately with your order details. We will initiate an investigation with the shipping carrier and work towards resolving the issue."
    },
    {
        "question": "Do you offer international shipping?",
        "answer": "Yes, we offer international shipping to many countries. During the checkout process, you can select your country for shipping options and rates."
    },
    {
        "question": "Can I request a specific delivery date for my order?",
        "answer": "While we cannot guarantee a specific delivery date, you can leave a note during the checkout process with your preferred delivery date, and we will do our best to accommodate it."
    },
    {
        "question": "How can I contact your customer service?",
        "answer": "You can contact our customer service by phone at +1-123-456-7890 or by email at support@logisticscompany.com. We are available to assist you during our business hours."
    },
    {
        "question": "What are your customer service hours?",
        "answer": "Our customer service is available from Monday to Friday, 9:00 AM to 5:00 PM (local time)."
    },
    {
        "question": "Do you offer live chat support?",
        "answer": "Yes, we offer live chat support on our website during our customer service hours. Look for the chat icon on our website to start a live chat with our support team."
    },
    {
        "question": "How long does it take to receive a response from customer service?",
        "answer": "We strive to respond to customer inquiries within 24 hours. However, during peak times, it may take slightly longer. We appreciate your patience."
    },
    {
        "question": "What information do I need to provide when contacting customer service?",
        "answer": "When contacting customer service, please provide your order number, the email address associated with your account, and a detailed description of your inquiry or issue."
    },
    {
        "question": "Can I request a change to my order after it has been placed?",
        "answer": "If you need to make changes to your order, such as adding or removing items, please contact our customer service as soon as possible, and we will check if the changes can be accommodated."
    },
    {
        "question": "What should I do if I receive the wrong item?",
        "answer": "If you receive the wrong item, please contact our customer service immediately with your order details and a description of the incorrect item, and we will arrange for a return or replacement."
    },
    {
        "question": "Are there any additional fees or customs duties for international shipments?",
        "answer": "Additional fees or customs duties may apply for international shipments depending on the destination country's regulations. Please check with your local customs office for more information."
    },
    {
        "question": "How can I provide feedback about the delivery experience?",
        "answer": "We value your feedback about the delivery experience. You can provide feedback by leaving a review on our website or contacting our customer service department."
    },
    {
        "question": "Can I track the status of my shipment?",
        "answer": "Yes, you can track the status of your shipment by entering the tracking number provided in the shipping confirmation email or by logging into your account on our website."
    },
    {
        "question": "What should I do if my package is damaged during transit?",
        "answer": "If your package is damaged during transit, please contact our customer service immediately and provide photos of the damaged package. We will assist you in resolving the issue and arranging for a replacement if necessary."
    },
    {
        "question": "Do you offer same-day delivery options?",
        "answer": "We may offer same-day delivery options in select areas. During the checkout process, you can check the availability of same-day delivery for your location."
    },
    {
        "question": "Can I request a specific delivery time window for my order?",
        "answer": "While we cannot guarantee a specific delivery time window, you can track your shipment to get an estimated delivery window. Some shipping carriers may offer delivery notifications or options to reschedule delivery."
    },
    {
        "question": "What should I do if my package is delayed?",
        "answer": "If your package is delayed, we apologize for the inconvenience. Please track your shipment for updates, and if there is a significant delay, contact our customer service for assistance."
    },
    {
        "question": "Can I return an item if I change my mind?",
        "answer": "Yes, you can return an item if you change your mind, as long as it is within the return period specified in our return policy. Please contact our customer service to initiate the return process."
    },
    {
        "question": "How can I provide feedback about the overall ordering experience?",
        "answer": "We value your feedback about the overall ordering experience. You can provide feedback by leaving a review on our website or contacting our customer service department."
    },
    {
        "question": "What should I do if I have a complaint about a customer service representative?",
        "answer": "If you have a complaint about a customer service representative, please contact our customer service department with the details of your complaint, and we will investigate the matter thoroughly."
    },
    {
        "question": "Can I request a refund for a damaged item?",
        "answer": "Yes, if you receive a damaged item, please contact our customer service immediately with photos of the damaged item. We will assess the situation and provide you with a refund or replacement."
    },
    {
        "question": "What should I do if my package is lost?",
        "answer": "If your package is lost, please contact our customer service immediately with your order details. We will initiate an investigation with the shipping carrier and work towards resolving the issue."
    },
    {
        "question": "Do you offer package consolidation for multiple orders?",
        "answer": "Yes, we offer package consolidation services for multiple orders. Please contact our customer service for assistance with consolidating your orders into a single shipment."
    },
    {
        "question": "Can I request a specific delivery person for my package?",
        "answer": "Unfortunately, we cannot accommodate requests for specific delivery personnel. The delivery person is assigned based on the shipping carrier's logistics and availability."
    },
    {
        "question": "How can I update my shipping address?",
        "answer": "To update your shipping address, please contact our customer service as soon as possible with your order details and the new shipping address. We will check if the update can be made before the package is shipped."
    },
    {
        "question": "What should I do if my package is missing items?",
        "answer": "If your package is missing items, please contact our customer service immediately with your order details and a description of the missing items. We will investigate the issue and rectify it as soon as possible."
    },
    {
        "question": "Do you offer gift wrapping services?",
        "answer": "Yes, we offer gift wrapping services for an additional fee. During the checkout process, you can select the gift wrapping option and provide any specific instructions."
    },
    {
        "question": "Can I request a specific delivery date for a gift order?",
        "answer": "While we cannot guarantee a specific delivery date for a gift order, you can leave a note during the checkout process with your preferred delivery date, and we will do our best to accommodate it."
    },
    {
        "question": "How can I cancel my order?",
        "answer": "To cancel your order, please contact our customer service as soon as possible with your order details. We will check if the cancellation can be processed before the package is shipped."
    },
    {
        "question": "What should I do if I receive a defective item?",
        "answer": "If you receive a defective item, please contact our customer service immediately with your order details and a description of the defect. We will arrange for a return or replacement."
    },
    {
        "question": "Can I request a signature requirement for delivery?",
        "answer": "Yes, you can request a signature requirement for delivery. During the checkout process, you can select the option for a signature upon delivery."
    },
    {
        "question": "What should I do if my package is delayed in customs?",
        "answer": "If your package is delayed in customs, it is typically awaiting clearance by the customs authorities. Please allow some time for the clearance process. If there are any issues, our customer service will assist you in resolving them."
    },
    {
        "question": "Do you offer bulk shipping discounts?",
        "answer": "Yes, we offer bulk shipping discounts for large orders or businesses. Please contact our customer service or sales department for more information on bulk shipping discounts."
    },
    {
        "question": "Can I change the shipping address for a gift order?",
        "answer": "To change the shipping address for a gift order, please contact our customer service as soon as possible with your order details and the new shipping address. We will check if the change can be made before the package is shipped."
    },
    {
        "question": "How can I provide feedback about the packaging of my order?",
        "answer": "We appreciate your feedback about the packaging of your order. You can provide feedback by leaving a review on our website or contacting our customer service department."
    }
]


    # Add user data to previous questions and answers
    for data in user_data:
        previous_questions_and_answers.append((data["question"], data["answer"]))

    while True:
        # ask the user for their question
        new_question = input(
            Fore.GREEN + Style.BRIGHT + "Customer: " + Style.RESET_ALL
        )
        # check the question is safe
        errors = get_moderation(new_question)
        if errors:
            print(
                Fore.RED
                + Style.BRIGHT
                + "Sorry, your question didn't pass the moderation check:"
            )
            for error in errors:
                print(error)
            print(Style.RESET_ALL)
            continue
        response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)

        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, response))

        # print the response
        print(Fore.CYAN + Style.BRIGHT + "Chat Assistant: " + Style.NORMAL + response)


if __name__ == "__main__":
    main()
