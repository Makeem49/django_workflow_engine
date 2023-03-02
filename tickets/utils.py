from .tasks import send_mail

def message_template(superior_officer, instance):
    """Message template"""
    message = f"""
                Hello {superior_officer}, a ticket an been raised, kindly check it out.\n 

                Ticket information:

                Ticket ID : {instance.ticket_id}
                Created at: {instance.date_updated}
                Created by: {instance.user.first_name} {instance.user.last_name}
                Department: {instance.user.department.name}
                Emaployee tag: {instance.user.employee_identification_tag}
                Employee level: {instance.user.level.name.capitalize()}

                Thanks. 
            """

    return message


def get_alert(level, instance, model, department):
    """
    levl: user level 
    instance : the save instance ticket
    model : User model for getting a particuler user
    department: department to get he department superior email 
    email: The ticket opener emal address 
    """
    if department and instance.publish: 

        if level == 'analyst':
            """Get the supervisor email attach to the department."""
            supervisor_email = department.supervisor.email
            message = message_template(department.supervisor.first_name, instance)
            """
            * Todo: Send email notifying the supervisor of the department an alert 
            """
            send_mail(instance.title, message, instance.user.email, supervisor_email)


        elif level == 'supervisor':
            """Get the head of department email."""
            head_of_department_email = department.head_of_department.email
            message = message_template(department.head_of_department.first_name, instance)


            """
            * Todo: Send email notifying the head of department an alert
            """
            send_mail(instance.title, message, instance.user.email, head_of_department_email)

        elif level == 'head of department':
            """Get the company cto/cfo email"""
            cto_or_cfo = model.objects.filter(level__name='CTO/CFO').first()
            cto_or_cfo_email = cto_or_cfo.email
            message = message_template(cto_or_cfo.first_name, instance)

            """
            * Todo: Send email to the cto/cfo of the company an alert 
            """
            send_mail(instance.title, message, instance.user.email, cto_or_cfo_email)

        elif level == 'cto/cfo':
            """Get the company president email"""
            president = model.objects.filter(level__name = 'President').first()
            president_email = president.email
            message = message_template(president.first_name, instance)

            """
            * Todo: Send email to the company president
            """
            send_mail(instance.title, message, instance.user.email, president_email)

        elif level == 'president':
            """Get the CEO email"""
            ceo = model.objects.filter(level__name = 'CEO').first()
            ceo_email = ceo.email 
            message = message_template(ceo.first_name, instance)

            """
            * Todo: Send email to the CEO of the president
            """                    
            send_mail(instance.title, message, instance.user.email, ceo_email)
