
prompt_enhancements =""""Suppose that we are working in the domain of a food delivery app.

the input data ( UserOrder, FoodIngredients, UserComment,) is only within the three backticks

UserComment expresses the user's satisfaction with the food quality and services delivered.

Having the context provided,
your task is to evaluate the food quality and services delivered based on UserComment and assign a score per each food and services delivered (an integer between 0 (for most disatisfies) and 5 (for most satisfied))considering the following rules:

Handle Mixed Sentiments:
If UserComment contains mixed sentiments (like positive followed by negative), consider the overall tone of the comment at its conclusion.
Focus on how the UserComment ends to determine if it’s generally positive or negative.
This prevents confusion over mixed messages within the comment.

1. Rate Food quality:

Analyze a user's comment to rate each food item in the UserOrder and the overall food experience.

Task:

1. Determine if the comment expresses satisfaction or dissatisfaction with the quality of any food item in the UserOrder.
2. Check if the comment directly mentions specific foods or food ingredients.
3. If the comment mentions a specific food from the UserOrder, rate that food based on the sentiment expressed.
4. If the comment mentions food ingredients, identify the food(s) containing those ingredients using the FoodIngredients list and rate that food based on the sentiment.
5. If the comment provides an overall assessment of the food experience without specifying a particular food item, only rate the "foods overall rating" score as the general order rating.
6. If the comment does not mention a specific food item, set the score for that food item to 'Nan'.
7. Apply the 'Handle Mixed Sentiments' rule when rating each food item and the overall food experience.

note : "foods overall rating" is not the average value of the food items


Important: if the comment says that a food item was raw (in persian:  خام  ) consider a low score for that food item. also  افتضاح  means awful.


Note: Ensure that each food item in the UserOrder receives a score, and an additional rating is provided for the "foods overall rating".


2. rate Service Quality :

Analyze a user's comment to rate  service categories:


1. Staff Behavior : Look for mentions of driver, delivery person,

2. Delivery Time: Analyze the comment for any mention of time related words or phrases  as "late", "fast", "on time", "delayed", "soon"  If found, assign a score.

3. Food Temperature: Look for words indicating temperature such as "hot", "cold", "warm", Assign a score based on the sentiment expressed about the food temperature

4. Delivered Food not as Ordered : Look for phrases indicating the food was not as ordered such as "wrong order", "not what I ordered", etc. Assign a score based on the sentiment expressed

5. packaging : Identify comments that mention the condition of the packaging when it arrived. Keywords might include “well-packed”, “leaking”, or “damaged”.

6. Cost of Delivery: Look for any mention of the delivery fee or cost. Phrases like “expensive delivery”, “cheap delivery”, or “free delivery” can be relevant.

7. Cost per Value of Foods: This involves comments about whether the user felt they got their money’s worth for the food they ordered. Relevant phrases could be ( "expensive"= " گران " ) “worth the price”, “overpriced”, or “good value”.


Important: food quality is not  part of the service ratings.

Remember, if the comment doesn’t mention services or fit any category, or if the sentiment is unclear, keep the service part empty in the JSON.
do not add any new categories to the service ratings.

3. Evaluate Food Temperature:

Analyze the UserComment to evaluate the temperature of the food.

Task:

1. Check if the UserComment mentions the temperature of a specific food item.
2. Identify the food item being discussed and determine its typical serving temperature (hot or cold).
3. Evaluate the UserComment to determine if the food temperature was satisfactory.
	If the food is typically served hot, but the comment indicates it was ' سرد ' (cold) assign a low temperature score.
	If the food is typically served warm, and the comment indicates it was ' گرم ' (warm), assign a higher temperature score.
	If the food temperature matches its typical serving temperature, assign a higher temperature score.
4. Update the services ratings with the evaluated food temperature score.

Note: Consider the typical serving temperature of different food types, such as hot for fast foods and main dishes, and cold for drinks and salads.


ATTENTION :
As you see, the UserComment is in Persian. Thus, be mindful of any different Persian idioms or slang used and their actual meanings.
don't translate food names


Based on the analysis, generate JSON for foods and services in this format:

{{
    "foods overall rating": <foods overall quality rating>,

    qualities: [
        {{
            "food_title": <food_title>,
            "food_rate": <food_rate>
        }}
    ],


    services: [
        {{
            {{
            "part_of_comment": <part_of_comment>,
            "service_rate": <service_rate>,
            "service_category": <service_category>
        }}
        }}

    ]
}}

```
Here is the list of foods and beverages ordered by a user, let's call it 'UserOrder':

UserOrder: {order}

If available, here is the  of ingredients for each or some food included in the UserOrder (called 'FoodIngredients'):
FoodIngredientsFoodIngredients: {ingredients}

here is the user's comment (review) about their experience with UserOrder (called 'UserComment'):

UserComment: {comment}
```

the "food_title" must be in the UserOrder and not in english

Explain the analysis first and then provide the JSON format.  """




system_role = "You are a helpful digital assisstant having brilliant analytical skills."
def get_prompt():
    global prompt_enhancements
    return prompt_enhancements

def get_system_role():
    global system_role
    return system_role
