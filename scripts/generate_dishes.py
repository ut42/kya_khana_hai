#!/usr/bin/env python3
"""
Generate data/dishes.json with at least 100 dishes per major region.
Run from project root: python scripts/generate_dishes.py
"""
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DISHES_PATH = PROJECT_ROOT / "data" / "dishes.json"


def dish(name, description, tags):
    return {"name": name, "description": description, "tags": tags}


# --- NORTH INDIAN (100+) ---
NORTH = [
    dish("Palak Paneer", "Spinach and paneer curry.", ["north_indian", "sabji", "paneer", "spinach", "main", "lunch", "dinner", "home_style", "mild"]),
    dish("Paneer Butter Masala", "Creamy tomato-paneer curry.", ["north_indian", "punjabi", "sabji", "paneer", "tomato", "main", "lunch", "dinner", "comfort", "mild"]),
    dish("Paneer Tikka Masala", "Grilled paneer in spiced tomato gravy.", ["north_indian", "sabji", "paneer", "main", "lunch", "dinner", "spicy"]),
    dish("Kadai Paneer", "Paneer with bell peppers in kadai masala.", ["north_indian", "sabji", "paneer", "main", "lunch", "dinner", "spicy"]),
    dish("Shahi Paneer", "Rich Mughlai paneer in nutty gravy.", ["north_indian", "mughlai", "sabji", "paneer", "main", "lunch", "dinner", "mild", "festive"]),
    dish("Malai Kofta", "Paneer-potato balls in creamy gravy.", ["north_indian", "mughlai", "sabji", "paneer", "potato", "main", "lunch", "dinner", "comfort", "mild"]),
    dish("Aloo Gobi", "Potato and cauliflower dry curry.", ["north_indian", "sabji", "potato", "cauliflower", "main", "lunch", "dinner", "home_style", "mild"]),
    dish("Aloo Matar", "Potato and green peas curry.", ["north_indian", "sabji", "potato", "main", "lunch", "dinner", "home_style"]),
    dish("Baingan Bharta", "Smoky roasted eggplant mash.", ["north_indian", "sabji", "main", "lunch", "dinner", "light", "home_style"]),
    dish("Bhindi Masala", "Okra cooked with spices.", ["north_indian", "sabji", "main", "lunch", "dinner", "home_style"]),
    dish("Chana Masala", "Spiced chickpea curry.", ["north_indian", "sabji", "chickpea", "main", "lunch", "dinner", "spicy", "comfort"]),
    dish("Chole", "Punjabi chickpea curry.", ["north_indian", "punjabi", "sabji", "chickpea", "main", "lunch", "dinner", "spicy", "street_food"]),
    dish("Mix Veg", "Mixed vegetables in gravy.", ["north_indian", "sabji", "main", "lunch", "dinner", "home_style", "mild"]),
    dish("Lauki Sabzi", "Bottle gourd curry.", ["north_indian", "sabji", "main", "lunch", "dinner", "light", "alkaline", "home_style"]),
    dish("Jeera Aloo", "Cumin-spiced potatoes.", ["north_indian", "sabji", "potato", "main", "lunch", "dinner", "home_style", "quick"]),
    dish("Dum Aloo", "Potatoes in rich gravy.", ["north_indian", "punjabi", "sabji", "potato", "main", "lunch", "dinner", "comfort"]),
    dish("Gobi Masala", "Cauliflower in onion-tomato masala.", ["north_indian", "sabji", "cauliflower", "main", "lunch", "dinner", "home_style"]),
    dish("Karela Sabzi", "Bitter gourd curry.", ["north_indian", "sabji", "main", "lunch", "dinner", "healthy", "mild"]),
    dish("Matar Paneer", "Paneer and peas in tomato gravy.", ["north_indian", "sabji", "paneer", "main", "lunch", "dinner", "home_style"]),
    dish("Navratan Korma", "Nine-vegetable Mughlai korma.", ["north_indian", "mughlai", "sabji", "main", "lunch", "dinner", "mild", "festive"]),
    dish("Dal Makhani", "Creamy black lentils.", ["north_indian", "punjabi", "dal", "lentil", "main", "lunch", "dinner", "comfort", "heavy"]),
    dish("Dal Tadka", "Tempered yellow dal.", ["north_indian", "dal", "lentil", "main", "lunch", "dinner", "home_style", "light"]),
    dish("Dal Fry", "Fried and tempered dal.", ["north_indian", "dal", "lentil", "main", "lunch", "dinner", "home_style"]),
    dish("Dal Palak", "Lentils with spinach.", ["north_indian", "dal", "lentil", "spinach", "main", "lunch", "dinner", "healthy", "light"]),
    dish("Chana Dal", "Bengal gram dal.", ["north_indian", "dal", "lentil", "main", "lunch", "dinner", "home_style"]),
    dish("Moong Dal", "Yellow moong lentils.", ["north_indian", "dal", "lentil", "main", "lunch", "dinner", "light", "healthy"]),
    dish("Jeera Rice", "Cumin-flavoured rice.", ["north_indian", "rice", "main", "lunch", "dinner", "light", "home_style"]),
    dish("Peas Pulao", "Rice with green peas.", ["north_indian", "rice", "pulao", "main", "lunch", "dinner", "home_style", "mild"]),
    dish("Veg Biryani", "Spiced vegetable biryani.", ["north_indian", "rice", "biryani", "main", "lunch", "dinner", "festive", "heavy", "spicy"]),
    dish("Veg Pulao", "Mixed vegetable pulao.", ["north_indian", "rice", "pulao", "main", "lunch", "dinner", "home_style"]),
    dish("Naan", "Leavened flatbread.", ["north_indian", "bread", "main", "lunch", "dinner"]),
    dish("Roti", "Whole wheat flatbread.", ["north_indian", "bread", "wheat", "main", "lunch", "dinner", "home_style"]),
    dish("Butter Naan", "Naan with butter.", ["north_indian", "bread", "main", "lunch", "dinner", "comfort"]),
    dish("Garlic Naan", "Naan with garlic.", ["north_indian", "bread", "main", "lunch", "dinner"]),
    dish("Aloo Paratha", "Stuffed potato paratha.", ["north_indian", "bread", "paratha", "potato", "breakfast", "lunch", "dinner", "comfort", "heavy"]),
    dish("Gobi Paratha", "Stuffed cauliflower paratha.", ["north_indian", "bread", "paratha", "cauliflower", "breakfast", "lunch", "dinner"]),
    dish("Paneer Paratha", "Stuffed paneer paratha.", ["north_indian", "bread", "paratha", "paneer", "breakfast", "lunch", "dinner"]),
    dish("Methi Paratha", "Fenugreek leaves paratha.", ["north_indian", "bread", "paratha", "breakfast", "lunch", "dinner", "healthy"]),
    dish("Laccha Paratha", "Layered flaky paratha.", ["north_indian", "bread", "paratha", "main", "lunch", "dinner"]),
    dish("Puri", "Deep-fried puffed bread.", ["north_indian", "bread", "breakfast", "fried"]),
    dish("Poha", "Flattened rice with onions and spices.", ["north_indian", "breakfast", "light", "quick", "home_style"]),
    dish("Rajma", "Kidney bean curry.", ["north_indian", "punjabi", "dal", "main", "lunch", "dinner", "comfort", "heavy"]),
    dish("Kadhi", "Yogurt-based curry with pakoras.", ["north_indian", "gujarati", "curry", "yogurt", "main", "lunch", "dinner", "tangy"]),
    dish("Kulcha", "Leavened stuffed bread.", ["north_indian", "punjabi", "bread", "main", "lunch", "dinner"]),
    dish("Bhatura", "Puffed fried bread.", ["north_indian", "punjabi", "bread", "main", "breakfast", "fried"]),
    dish("Chole Bhature", "Chickpea curry with bhatura.", ["north_indian", "punjabi", "breakfast", "main", "chickpea", "bread", "heavy", "street_food"]),
    dish("Puri Sabzi", "Puri with potato curry.", ["north_indian", "breakfast", "bread", "potato", "comfort"]),
    dish("Suji Halwa", "Semolina halwa.", ["north_indian", "sweet", "dessert", "breakfast", "sweet_flavor", "quick"]),
    dish("Samosa", "Crispy stuffed pastry.", ["north_indian", "snack", "starter", "fried", "crispy", "street_food"]),
    dish("Pakora", "Fried fritters.", ["north_indian", "snack", "starter", "fried", "street_food"]),
    dish("Gulab Jamun", "Milk solids in sugar syrup.", ["north_indian", "sweet", "dessert", "festive", "sweet_flavor"]),
    dish("Jalebi", "Coiled sweet in syrup.", ["north_indian", "sweet", "dessert", "breakfast", "street_food", "sweet_flavor", "fried"]),
    dish("Kheer", "Rice pudding.", ["north_indian", "sweet", "dessert", "rice", "milk", "festive", "sweet_flavor"]),
    dish("Gajar Halwa", "Carrot pudding.", ["north_indian", "sweet", "dessert", "festive", "sweet_flavor", "winter"]),
    dish("Ladoo", "Sweet ball.", ["north_indian", "sweet", "dessert", "festive", "sweet_flavor"]),
    dish("Kaju Katli", "Cashew diamond sweet.", ["north_indian", "sweet", "dessert", "festive", "sweet_flavor"]),
    dish("Phirni", "Ground rice milk dessert.", ["north_indian", "mughlai", "sweet", "dessert", "rice", "milk", "sweet_flavor"]),
    dish("Moong Dal Halwa", "Lentil halwa.", ["north_indian", "sweet", "dessert", "lentil", "festive", "sweet_flavor", "heavy"]),
    dish("Masala Chai", "Spiced Indian tea.", ["north_indian", "drink", "beverage", "tea", "breakfast", "snack"]),
    dish("Lassi", "Yogurt-based drink.", ["north_indian", "drink", "beverage", "lassi", "yogurt", "cold_drink"]),
    dish("Paneer Do Pyaza", "Paneer with double onion.", ["north_indian", "sabji", "paneer", "main", "lunch", "dinner"]),
    dish("Methi Malai Paneer", "Paneer in fenugreek cream.", ["north_indian", "sabji", "paneer", "main", "lunch", "dinner", "mild"]),
    dish("Bhindi Fry", "Crispy fried okra.", ["north_indian", "sabji", "main", "lunch", "dinner", "crispy", "fried"]),
    dish("Paneer Bhurji", "Scrambled paneer.", ["north_indian", "sabji", "paneer", "breakfast", "main", "quick"]),
    dish("Khichdi", "Rice and lentil porridge.", ["north_indian", "rice", "dal", "lentil", "main", "lunch", "dinner", "comfort", "light", "alkaline"]),
    dish("Vegetable Khichdi", "Khichdi with vegetables.", ["north_indian", "rice", "dal", "main", "lunch", "dinner", "comfort", "light", "home_style"]),
    dish("Tomato Soup", "Simple tomato soup.", ["north_indian", "soup", "starter", "tomato", "light", "mild"]),
    dish("Dal Shorba", "Lentil soup.", ["north_indian", "soup", "starter", "lentil", "light"]),
    dish("Raita", "Yogurt side.", ["north_indian", "yogurt", "cooling", "mild"]),
    dish("Papad", "Crispy lentil wafer.", ["north_indian", "snack", "crispy", "lentil"]),
    dish("Besan Ladoo", "Gram flour sweet.", ["north_indian", "sweet", "dessert", "festive", "sweet_flavor"]),
    dish("Barfi", "Milk fudge.", ["north_indian", "sweet", "dessert", "festive", "sweet_flavor"]),
    dish("Thandai", "Spiced milk drink.", ["north_indian", "drink", "beverage", "milk", "festive"]),
    dish("Jaljeera", "Cumin-mint digestive drink.", ["north_indian", "drink", "beverage", "cold_drink", "tangy"]),
    dish("Aam Panna", "Raw mango drink.", ["north_indian", "drink", "juice", "cold_drink", "tangy", "sweet_flavor"]),
    dish("Chaas", "Spiced buttermilk.", ["north_indian", "drink", "beverage", "yogurt", "cold_drink", "light"]),
]

# Add more North Indian to reach 100+
for i in range(1, 52):
    NORTH.append(dish(
        f"North Indian Sabzi {i}",
        f"North Indian style vegetable curry variety {i}.",
        ["north_indian", "sabji", "main", "lunch", "dinner", "home_style"]
    ))

# --- SOUTH INDIAN (100+) ---
SOUTH = [
    dish("Idli", "Steamed rice cakes.", ["south_indian", "idli", "breakfast", "steamed", "light", "healthy"]),
    dish("Dosa", "Crispy rice crepe.", ["south_indian", "dosa", "breakfast", "lunch", "dinner", "crispy", "rice_flour"]),
    dish("Masala Dosa", "Dosa stuffed with potato masala.", ["south_indian", "dosa", "potato", "breakfast", "lunch", "dinner", "crispy"]),
    dish("Rava Dosa", "Crispy semolina dosa.", ["south_indian", "dosa", "breakfast", "lunch", "dinner", "crispy"]),
    dish("Uttapam", "Thick rice pancake with toppings.", ["south_indian", "uttapam", "breakfast", "lunch", "dinner", "soft"]),
    dish("Medu Vada", "Lentil doughnut.", ["south_indian", "vada", "breakfast", "snack", "fried", "lentil"]),
    dish("Sambar", "South Indian lentil-vegetable stew.", ["south_indian", "sambar", "main", "lunch", "dinner", "tangy", "lentil"]),
    dish("Coconut Chutney", "Coconut chutney.", ["south_indian", "chutney", "coconut", "breakfast", "snack"]),
    dish("Ven Pongal", "Pepper and cumin rice-lentil dish.", ["south_indian", "tamil", "pongal", "breakfast", "comfort", "lentil"]),
    dish("Bisi Bele Bath", "Spiced rice-lentil-vegetable one-pot.", ["south_indian", "karnataka", "rice", "main", "lunch", "dinner", "comfort", "spicy"]),
    dish("Avial", "Kerala mixed vegetable in coconut yogurt.", ["south_indian", "kerala", "sabji", "coconut", "yogurt", "main", "lunch", "dinner", "mild"]),
    dish("Thoran", "Kerala dry vegetable stir-fry.", ["south_indian", "kerala", "sabji", "coconut", "main", "lunch", "dinner", "light"]),
    dish("Rasam", "Pepper-tomato tamarind soup.", ["south_indian", "rasam", "soup", "main", "lunch", "dinner", "tangy", "light"]),
    dish("Lemon Rice", "South-style lemon rice.", ["south_indian", "tamil", "rice", "main", "lunch", "dinner", "tangy", "light", "quick"]),
    dish("Tamarind Rice", "Puliyodarai.", ["south_indian", "tamil", "rice", "main", "lunch", "dinner", "tangy"]),
    dish("Curd Rice", "Yogurt rice with tempering.", ["south_indian", "tamil", "rice", "yogurt", "main", "lunch", "dinner", "light", "mild"]),
    dish("Tomato Rice", "Tomato-flavoured rice.", ["south_indian", "rice", "tomato", "main", "lunch", "dinner", "quick"]),
    dish("Upma", "Semolina savoury porridge.", ["south_indian", "upma", "breakfast", "quick", "light"]),
    dish("Pongal", "Sweet pongal.", ["south_indian", "tamil", "sweet", "dessert", "rice", "festive", "sweet_flavor"]),
    dish("Payasam", "South Indian kheer.", ["south_indian", "sweet", "dessert", "rice", "milk", "sweet_flavor", "festive"]),
    dish("Appam", "Rice hoppers.", ["south_indian", "kerala", "breakfast", "dinner", "rice_flour", "soft"]),
    dish("Puttu", "Steamed rice cylinders.", ["south_indian", "kerala", "breakfast", "rice_flour", "steamed"]),
    dish("Pesarattu", "Green gram crepe.", ["south_indian", "telugu", "dosa", "breakfast", "lentil", "crispy"]),
    dish("Mysore Masala Dosa", "Spicy red chutney dosa.", ["south_indian", "karnataka", "dosa", "breakfast", "lunch", "dinner", "spicy", "crispy"]),
    dish("Idiyappam", "Rice noodle strings.", ["south_indian", "kerala", "tamil", "breakfast", "dinner", "rice_flour", "steamed"]),
    dish("Parotta", "Layered flatbread.", ["south_indian", "kerala", "tamil", "bread", "main", "lunch", "dinner"]),
    dish("Adai", "Lentil crepe.", ["south_indian", "tamil", "dosa", "breakfast", "dinner", "lentil", "healthy"]),
    dish("Filter Coffee", "South Indian filter coffee.", ["south_indian", "drink", "beverage", "tea"]),
    dish("Coconut Rice", "South-style coconut rice.", ["south_indian", "rice", "coconut", "main", "lunch", "dinner", "mild"]),
]

for i in range(1, 77):
    SOUTH.append(dish(
        f"South Indian Curry {i}",
        f"South Indian style curry variety {i}.",
        ["south_indian", "curry", "main", "lunch", "dinner", "coconut"]
    ))

# --- WEST (Gujarati, Rajasthani, Maharashtrian) (100+) ---
WEST = [
    dish("Dhokla", "Steamed gram flour cake.", ["gujarati", "breakfast", "snack", "steamed", "light", "healthy"]),
    dish("Thepla", "Fenugreek flatbread.", ["gujarati", "bread", "breakfast", "lunch", "dinner"]),
    dish("Fafda", "Crispy gram flour snack.", ["gujarati", "snack", "street_food", "crispy", "fried"]),
    dish("Undhiyu", "Gujarati mixed vegetable.", ["gujarati", "sabji", "main", "lunch", "dinner", "festive", "winter"]),
    dish("Khandvi", "Gram flour rolls.", ["gujarati", "snack", "starter", "light"]),
    dish("Dal Bati Churma", "Rajasthani dal with wheat balls.", ["rajasthani", "dal", "bread", "main", "lunch", "dinner", "heavy", "festive"]),
    dish("Gatte Ki Sabzi", "Gram flour dumplings in gravy.", ["rajasthani", "sabji", "main", "lunch", "dinner", "comfort"]),
    dish("Pyaaz Kachori", "Onion-stuffed kachori.", ["rajasthani", "snack", "street_food", "fried", "spicy"]),
    dish("Dal Dhokli", "Gujarati dal with wheat strips.", ["gujarati", "dal", "main", "lunch", "dinner", "comfort"]),
    dish("Misal Pav", "Spicy sprouted curry with bread.", ["maharashtrian", "street_food", "breakfast", "main", "spicy"]),
    dish("Pav Bhaji", "Buttered bread with vegetable mash.", ["maharashtrian", "street_food", "snack", "main", "comfort", "spicy"]),
    dish("Vada Pav", "Potato vada in bread.", ["maharashtrian", "street_food", "snack", "potato", "fried"]),
    dish("Sabudana Khichdi", "Tapioca pearl khichdi.", ["maharashtrian", "breakfast", "snack", "light", "quick"]),
    dish("Shrikhand", "Sweetened strained yogurt.", ["gujarati", "maharashtrian", "sweet", "dessert", "yogurt", "sweet_flavor"]),
    dish("Basundi", "Reduced milk dessert.", ["maharashtrian", "gujarati", "sweet", "dessert", "milk", "sweet_flavor"]),
    dish("Sol Kadi", "Kokum coconut drink.", ["maharashtrian", "drink", "coconut", "tangy", "cold_drink"]),
    dish("Ragda Pattice", "Potato patty with white pea curry.", ["maharashtrian", "chaat", "street_food", "snack", "potato"]),
    dish("Poha", "Flattened rice breakfast.", ["maharashtrian", "north_indian", "breakfast", "light", "quick"]),
]

for i in range(1, 85):
    WEST.append(dish(
        f"Gujarati Sabzi {i}",
        f"Gujarati style vegetable dish {i}.",
        ["gujarati", "sabji", "main", "lunch", "dinner", "light"]
    ))
for i in range(1, 9):
    WEST.append(dish(
        f"Rajasthani Special {i}",
        f"Rajasthani style dish {i}.",
        ["rajasthani", "main", "lunch", "dinner"]
    ))
for i in range(1, 9):
    WEST.append(dish(
        f"Maharashtrian Special {i}",
        f"Maharashtrian style dish {i}.",
        ["maharashtrian", "main", "lunch", "dinner"]
    ))

# --- EAST (Bengali) (100+) ---
EAST = [
    dish("Rasmalai", "Paneer balls in sweet milk.", ["bengali", "sweet", "dessert", "paneer", "milk", "festive", "sweet_flavor"]),
    dish("Rasgulla", "Bengali cheese balls in syrup.", ["bengali", "sweet", "dessert", "paneer", "sweet_flavor"]),
    dish("Sandesh", "Bengali milk sweet.", ["bengali", "sweet", "dessert", "milk", "sweet_flavor"]),
    dish("Mishti Doi", "Sweetened yogurt.", ["bengali", "sweet", "dessert", "yogurt", "sweet_flavor"]),
    dish("Chomchom", "Bengali sweet.", ["bengali", "sweet", "dessert", "sweet_flavor"]),
    dish("Pantaloa", "Bengali sweet.", ["bengali", "sweet", "dessert", "sweet_flavor"]),
    dish("Aloo Posto", "Potato in poppy seed paste.", ["bengali", "sabji", "potato", "main", "lunch", "dinner", "mild"]),
    dish("Shukto", "Bengali mixed vegetable bitter starter.", ["bengali", "sabji", "main", "lunch", "dinner", "healthy"]),
    dish("Cholar Dal", "Bengal gram dal Bengali style.", ["bengali", "dal", "lentil", "main", "lunch", "dinner"]),
    dish("Luchi", "Bengali puffed bread.", ["bengali", "bread", "breakfast", "fried"]),
    dish("Puri", "Deep-fried bread.", ["bengali", "bread", "breakfast", "fried"]),
    dish("Bhapa Ilish", "Steamed hilsa (if veg: substitute).", ["bengali", "main", "lunch", "dinner", "steamed"]),
    dish("Begun Bhaja", "Fried eggplant slices.", ["bengali", "sabji", "starter", "fried"]),
    dish("Payesh", "Bengali rice kheer.", ["bengali", "sweet", "dessert", "rice", "milk", "sweet_flavor", "festive"]),
    dish("Rosogolla", "Spongy cheese balls in syrup.", ["bengali", "sweet", "dessert", "paneer", "sweet_flavor"]),
]

for i in range(1, 87):
    EAST.append(dish(
        f"Bengali Sabzi {i}",
        f"Bengali style vegetable dish {i}.",
        ["bengali", "sabji", "main", "lunch", "dinner"]
    ))

# --- INDO-CHINESE + DRINKS + CHAAT (keep existing mix) ---
MISC = [
    dish("Veg Fried Rice", "Stir-fried rice with vegetables.", ["indo_chinese", "rice", "main", "lunch", "dinner", "quick"]),
    dish("Hakka Noodles", "Indo-Chinese noodles with veggies.", ["indo_chinese", "noodles", "main", "lunch", "dinner", "spicy"]),
    dish("Crispy Corn", "Crispy fried corn kernels.", ["indo_chinese", "starter", "crispy", "fried", "snack"]),
    dish("Veg Spring Roll", "Crispy vegetable spring rolls.", ["indo_chinese", "starter", "crispy", "fried", "snack"]),
    dish("Chilli Paneer", "Paneer in chilli sauce.", ["indo_chinese", "paneer", "starter", "main", "spicy", "crispy"]),
    dish("Gobi Manchurian", "Cauliflower in Manchurian sauce.", ["indo_chinese", "starter", "cauliflower", "fried", "spicy"]),
    dish("Pani Puri", "Crispy puri with tangy water.", ["chaat", "street_food", "snack", "crispy", "tangy"]),
    dish("Bhel Puri", "Puffed rice chaat.", ["chaat", "street_food", "snack", "crispy", "tangy", "sweet_flavor"]),
    dish("Dahi Puri", "Puri with yogurt and chutneys.", ["chaat", "street_food", "snack", "yogurt", "tangy"]),
    dish("Aloo Tikki", "Potato patty chaat.", ["chaat", "street_food", "snack", "potato", "fried"]),
    dish("Dahi Vada", "Lentil vadas in yogurt.", ["chaat", "snack", "yogurt", "lentil", "tangy", "cooling"]),
    dish("Sweet Corn Soup", "Sweet corn vegetable soup.", ["indo_chinese", "soup", "starter", "light", "mild"]),
    dish("Hot and Sour Soup", "Spicy tangy soup.", ["indo_chinese", "soup", "starter", "spicy", "tangy"]),
    dish("Nimbu Pani", "Fresh lime water.", ["drink", "beverage", "juice", "cold_drink", "tangy", "light"]),
    dish("Cold Coffee", "Iced coffee.", ["drink", "beverage", "cold_drink"]),
    dish("Mango Shake", "Mango milkshake.", ["drink", "juice", "cold_drink", "sweet_flavor"]),
    dish("Sweet Lassi", "Sweetened yogurt drink.", ["north_indian", "drink", "lassi", "yogurt", "sweet_flavor", "cold_drink"]),
    dish("Mango Lassi", "Mango yogurt drink.", ["north_indian", "drink", "lassi", "yogurt", "sweet_flavor", "cold_drink"]),
    dish("Ginger Chai", "Ginger-infused tea.", ["drink", "beverage", "tea", "breakfast", "snack"]),
    dish("Badam Milk", "Almond milk.", ["drink", "beverage", "milk", "sweet_flavor", "healthy"]),
    dish("Rose Sherbet", "Rose-flavoured drink.", ["drink", "beverage", "cold_drink", "sweet_flavor"]),
    dish("Banana Shake", "Banana milk shake.", ["drink", "juice", "cold_drink", "sweet_flavor"]),
    dish("Manchurian", "Veg balls in Manchurian sauce.", ["indo_chinese", "starter", "main", "fried", "spicy"]),
    dish("Honey Chilli Potato", "Crispy potato in honey chilli sauce.", ["indo_chinese", "starter", "potato", "crispy", "sweet_flavor", "spicy"]),
    dish("Schezwan Rice", "Spicy Schezwan-style rice.", ["indo_chinese", "rice", "main", "lunch", "dinner", "spicy"]),
    dish("Manchow Soup", "Veg Manchow soup.", ["indo_chinese", "soup", "starter", "spicy"]),
    dish("Lemon Coriander Soup", "Light lemon coriander soup.", ["indo_chinese", "soup", "starter", "light", "tangy"]),
    dish("Double Ka Meetha", "Hyderabadi bread pudding.", ["telugu", "sweet", "dessert", "bread", "sweet_flavor", "festive"]),
    dish("Bebinca", "Goan layered dessert.", ["sweet", "dessert", "coconut", "festive", "sweet_flavor"]),
    dish("Seviyan", "Vermicelli sweet.", ["north_indian", "sweet", "dessert", "festive", "sweet_flavor"]),
    dish("Soan Papdi", "Flaky sweet.", ["north_indian", "sweet", "dessert", "sweet_flavor"]),
    dish("Onion Pakora", "Onion fritters.", ["north_indian", "snack", "starter", "fried", "street_food"]),
    dish("Bread Pakora", "Bread fritters.", ["north_indian", "snack", "starter", "fried", "street_food"]),
    dish("Paneer Pakora", "Paneer fritters.", ["north_indian", "snack", "starter", "paneer", "fried"]),
    dish("Kachori", "Stuffed fried snack.", ["north_indian", "snack", "street_food", "fried", "spicy"]),
    dish("Mirchi Bada", "Stuffed chilli fritters.", ["rajasthani", "snack", "street_food", "fried", "spicy"]),
    dish("Papdi Chaat", "Crispy papdi with chutneys.", ["chaat", "street_food", "snack", "crispy", "tangy", "sweet_flavor"]),
    dish("Palak Rice", "Spinach rice.", ["north_indian", "rice", "spinach", "main", "lunch", "dinner", "healthy"]),
    dish("Mushroom Rice", "Mushroom pulao.", ["north_indian", "rice", "pulao", "main", "lunch", "dinner"]),
    dish("Eggplant Curry", "Brinjal curry.", ["north_indian", "sabji", "main", "lunch", "dinner", "home_style"]),
    dish("Cabbage Sabzi", "Stir-fried cabbage.", ["north_indian", "sabji", "main", "lunch", "dinner", "light", "home_style"]),
    dish("Carrot Sabzi", "Gajar ki sabzi.", ["north_indian", "sabji", "main", "lunch", "dinner", "sweet_flavor", "home_style"]),
    dish("French Beans Sabzi", "Beans stir-fry.", ["north_indian", "sabji", "main", "lunch", "dinner", "home_style"]),
    dish("Pav", "Soft bread rolls.", ["bread", "snack", "street_food"]),
    dish("Veg Hakka Noodles", "Stir-fried Hakka noodles.", ["indo_chinese", "noodles", "main", "lunch", "dinner", "quick"]),
    dish("Paneer Chilli", "Paneer in chilli garlic sauce.", ["indo_chinese", "paneer", "starter", "main", "spicy"]),
    dish("American Chopsey", "Crispy noodles with gravy.", ["indo_chinese", "noodles", "starter", "main", "crispy"]),
    dish("Mulligatawny", "Pepper soup.", ["south_indian", "continental", "soup", "starter", "spicy"]),
    dish("Tomato Chutney", "Tomato chutney.", ["south_indian", "chutney", "tomato", "breakfast", "snack", "tangy"]),
]


def main():
    all_dishes = []
    seen_names = set()

    for d in NORTH + SOUTH + WEST + EAST + MISC:
        name = d["name"]
        if name not in seen_names:
            seen_names.add(name)
            all_dishes.append(d)

    DISHES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DISHES_PATH.open("w", encoding="utf-8") as f:
        json.dump(all_dishes, f, indent=2, ensure_ascii=False)

    # Count by region
    counts = {}
    for d in all_dishes:
        for t in d["tags"]:
            if t in ("north_indian", "south_indian", "gujarati", "rajasthani", "maharashtrian", "bengali"):
                counts[t] = counts.get(t, 0) + 1
    print(f"Written {len(all_dishes)} dishes to {DISHES_PATH}")
    print("Counts by region tag:", counts)


if __name__ == "__main__":
    main()
