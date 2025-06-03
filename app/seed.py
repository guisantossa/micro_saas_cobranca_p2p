import os
import random
from datetime import datetime, timedelta

import django
import faker
from core.models import (  # Ajusta 'yourapp' pro nome correto do app
    Charge,
    Installment,
    Payment,
)
from users.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

django.setup()


fake = faker.Faker("pt_BR")


def random_cpf():
    # Faker já tem cpf, mas tem que formatar para seu modelo (ex: 11 dígitos)
    return fake.cpf().replace(".", "").replace("-", "")


def create_users(n=300):
    users = []
    for _ in range(n):
        cpf = random_cpf()
        email = fake.unique.email()
        name = fake.name()
        phone = fake.msisdn()[
            :11
        ]  # só os primeiros 11 dígitos pra combinar com seu campo
        address = fake.street_address()
        zipcode = fake.postcode().replace("-", "")
        city = fake.city()
        state = fake.state_abbr()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=75)
        gender = random.choice(["M", "F"])

        user = User(
            cpf=cpf,
            email=email,
            name=name,
            phone=phone,
            address=address,
            zipcode=zipcode,
            city=city,
            state=state,
            birth_date=birth_date,
            gender=gender,
            is_active=True,
            is_staff=False,
        )
        user.set_password("123456")  # senha padrão só pra garantir
        users.append(user)
    User.objects.bulk_create(users)
    return User.objects.all()


def create_charges_for_users(users):
    status_choices = ["Pending", "Paid", "Cancelled"]
    payment_methods = ["Pix", "Boleto", "Transfer", "Cash"]
    for user in users:
        charge_count = random.randint(2, 5)
        if random.random() < 0.1:  # 10% dos usuários podem ter até 10 cobranças
            charge_count = random.randint(6, 10)
        for _ in range(charge_count):
            total_amount = round(random.uniform(50, 5000), 2)
            description = fake.sentence(nb_words=6)
            status = random.choice(status_choices)
            due_date = fake.date_between(start_date="-1y", end_date="+1y")
            installment_count = random.randint(1, 12)

            # Dados do devedor: vamos simular que é outro usuário, ou usar dados aleatórios
            debtor_name = fake.name()
            debtor_phone = fake.msisdn()[:11]
            debtor_email = fake.email()

            charge = Charge.objects.create(
                user=user,
                name=debtor_name,
                phone=debtor_phone,
                email=debtor_email,
                total_amount=total_amount,
                description=description,
                status=status,
                due_date=due_date,
                installment_count=installment_count,
            )

            # Criar as parcelas (installments)
            installment_amount = round(total_amount / installment_count, 2)
            for num in range(1, installment_count + 1):
                inst_due_date = due_date + timedelta(days=30 * (num - 1))
                inst_status = "Pending"
                if status == "Paid":
                    inst_status = "Paid"
                elif status == "Cancelled":
                    inst_status = "Cancelled"
                elif status == "Pending" and inst_due_date < datetime.now().date():
                    inst_status = "Overdue"

                installment = Installment.objects.create(
                    charge=charge,
                    number=num,
                    amount=installment_amount,
                    due_date=inst_due_date,
                    status=inst_status,
                )

                # Se parcela paga, criar pagamento
                if inst_status == "Paid":
                    payment_date = inst_due_date - timedelta(days=random.randint(0, 5))
                    Payment.objects.create(
                        installment=installment,
                        payment_date=payment_date,
                        amount_paid=installment_amount,
                        payment_method=random.choice(payment_methods),
                    )


if __name__ == "__main__":
    print("Gerando usuários...")
    users = create_users()
    print(f"{users.count()} usuários criados.")

    print("Gerando cobranças e parcelas...")
    create_charges_for_users(users)
    print("Seed completo.")
