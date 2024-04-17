from celery import shared_task
from accounts.models import CustomeUser

# @shared_task
# def test_tasks():
#     print ("test successfully in ")



# @shared_task
# def test_tasks2(day, week=0):
#     print (f"test successfully in {day} and {week}")

@shared_task
def clean_unverified_users():
    users = CustomeUser.objects.filter(is_verified=False)
    print ("teeeeeeeeeeest")
    users.delete()
    print ("teeeeeeeeeeest")