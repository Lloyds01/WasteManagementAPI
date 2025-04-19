# from django.db.models import Q
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User



# @receiver(post_save, sender=User)
# def create_recycle_agent(sender, instance, created, **kwargs):
#     if created:

#         print(instance.first_name)
        # recycle_agent = RecycleAgents.objects.create(
        #     user=instance,
        #     agent_assignment=AgentAssignment.objects.create(
        #         user=instance,
        #         agent=instance.agent,
        #     ),
        # )
        # recycle_agent.save()