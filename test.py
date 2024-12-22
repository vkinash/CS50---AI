# class Solution:
#     def twoSum(self, nums: list[int], target: int) -> list[int]:
#         # k = 1
#         # ln = len(nums)
#         # for i in range(ln):
#         #     if (target - nums[i]) in nums[k : ln]:
#         #         return [i, nums[k : ln].index(target - nums[i])+k]
#         #     k += 1
#         sum_dict = dict()
#
#         for i in range(len(nums)):
#             var = target - nums[i]
#
#             if sum_dict.get(var, None) != None:
#                 return [sum_dict[var], i]
#
#             sum_dict[nums[i]] = i
#
# print(Solution().twoSum([2,7,6,4], 9))

# class A():
#     def __init__(self, s):
#         self.s = s
#
#     def __eq__(self, other):
#         return self.s+"2" == other.s
#
# s1 = A("something")
# s2 = A("something2")
# print(s1==s2)
# height=8
# width=8
# cell = (7,0)
# possible_cells = set()
# row, column = cell
# for i in range(-1, 2):
#     idx_row = row + i
#     if 0 <= idx_row < height:
#         for j in range(-1, 2):
#             idx_column = column + j
#             if (idx_row != row or idx_column != column) and 0 <= idx_column < width:
#                 possible_cells.add((idx_row, idx_column))
# print(possible_cells)

j = {"Text with translations": [
    {
"id": 1,
"user": "+27636710051",
"ukr_massage": "Привіт   ! Я Адель, приємно познайомитися. Я з відділу кадрів у LinkedIn. Чи можу я мати кілька хвилин вашого часу?",
"en_translation:":
"Hello! I'm Adel, nice to meet you. I'm from the LinkedIn HR department. Can I have a few minutes of your time?"
    },
    {
"id": 2,
"user": "+27636710051",
"ukr_massage": "Це робота на неповний робочий день, яка не заважає вашій іншій роботі, робота проста, вам потрібно лише оцінити та переглянути наш магазин і надіслати нам знімки екрана, і ви отримаєте гроші. Ми платимо за це завдання 50 грн, а ви можете заробляти до 1500-3000 грн в день, оцінюючи та переглядаючи у вільний час.",
"en_translation": "This is a part-time job that won't interfere with your other work. It's simple: you just need to review and rate our store, then send us screenshots. We pay 50 UAH for this task, and you can earn up to 1500-3000 UAH a day, doing it in your free time.",
    },
    {
"id": 3,
"user": "Vladyslav Kinash",
"ukr_massage": "Доброго дня! Дякую за пропозицію. Чи могли би ви скинути лінк на вакансію та написати мені в лінкедін?",
"en_translation": "Good day! Thank you for the offer. Could you please send me the link to the job and message me on LinkedIn?"
    },
    {
"id": 4,
"user": "Vladyslav Kinash",
"ukr_massage": "Та ще прошу Вас вказати де саме в лінкедін Ви знайшли мій приватний номер? Тому що я намагаюсь його не вказувати у відкритих джерелах",
"en_translation": "Also, may I ask how you found my private number on LinkedIn? I try not to disclose it in public sources."
    },
    {
"id": 5,
"user": "+27636710051",
"ukr_massage": "Я дам вам 3 посилання на наш магазин, все, що вам потрібно зробити, це поставити 5 зірок з хорошим відгуком і надіслати мені скріншоти кожного завдання, і ви отримаєте свою першу зарплату в розмірі 50 грн. 1: https://maps.app.goo.gl/u1vtUETa5SVBbDX47 2: https://maps.app.goo.gl/QbyZKYR18McovWo36 3: https://maps.app.goo.gl/dksbigayCXngD4EY8",
"en_translation": "I'll provide you with three links to our store. All you need to do is give a 5-star rating with a positive review and send me screenshots of each task. You'll receive your first payment of 50 UAH. 1: https://maps.app.goo.gl/u1vtUETa5SVBbDX47 2: https://maps.app.goo.gl/QbyZKYR18McovWo36 3: https://maps.app.goo.gl/dksbigayCXngD4EY8"
    },
    {
"id": 6,
"user": "+27636710051",
"ukr_massage": "ваш номер вибирається нашою системою випадковим чином,",
"en_translation": "Your number is randomly selected by our system."
    },
    {
"id": 7,
"user": "+27636710051",
"ukr_massage": "ми співпрацюємо з linkedln",
"en_translation": "We collaborate with LinkedIn."
    }
]
}

import json

jj = json.dumps(j)
print(jj)