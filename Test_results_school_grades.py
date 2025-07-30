print("Write your name here: ")
name=input()
score=float(input("Welcome back, type your score here: ")) 

if score <= 3:
 print("Failed, retry again! Your score is: D-- ❄️ ")
elif score <= 5:
 print("Failed, C-- 🔒 ")
elif score <= 5.9:
 print("Failed, C- 😞 " )
elif score <= 6.0:
 print("Passed, B 🔐 ")
elif score <= 6.5:
 print("Passed, B+ 👌 ")
elif score <= 7:
 print("Passed, bravo!! Your score is : B++ 🤙 ")
elif score <= 8 :
 print("Passed, well done!!1your score is: A 🎖 ")
elif score <= 9:
 print("Passed with merits, A+ 🏵 ")
elif score <= 9.5:
 print("Passed with extra merits, S 🎊 ")
elif score == 10:
 print("Passed with giga merits, S++ 🥇 ")







