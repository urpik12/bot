from typing import List

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ComponentDialog,
)
from botbuilder.dialogs.choices.list_style import ListStyle
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions
from botbuilder.dialogs.choices import Choice
from botbuilder.core import CardFactory, MessageFactory

from botbuilder.schema import (
    Attachment,
    HeroCard,
    CardImage,
)


class ReviewKafedra(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(ReviewKafedra, self).__init__(
            dialog_id or ReviewKafedra.__name__
        )

        self.COMPANIES_SELECTED = "value-companiesSelected"
        self.DONE_OPTION = "done"

        self.list_of_choices = [
            Choice('Відео знайомство з ІМФН'),
            Choice('Відео про прикладну математику'),
            Choice('Презентація'),
            Choice('День відкритих дверей'),
            Choice('Навчальні лабораторії'),
            Choice('Навчальні дисципліни'),
            Choice('Соцмережі і сайти'),
            Choice('Контакти'),
            Choice('Назад')
        ]

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__, [self.selection_step, self.loop_step]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def selection_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        # prompt with the list of choices
        prompt_options = PromptOptions(
            prompt=MessageFactory.text("Підменю Про Кафедру"),
            # retry_prompt=MessageFactory.text("Please choose an option from the list"),
            choices=self.list_of_choices,
            style=ListStyle.hero_card,
            # style=ListStyle.suggested_action,
        )
        return await step_context.prompt(ChoicePrompt.__name__, prompt_options)

    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        chosen_option = step_context.result.value

        reply = MessageFactory.list([])
        test_reply_for_skype = MessageFactory.list([])

        if chosen_option == "Назад":
            return await step_context.end_dialog()

        elif chosen_option == "Відео знайомство з ІМФН":
            await step_context.context.send_activity(MessageFactory.text("https://www.youtube.com/watch?v=pCCmDBH50yc"))

        elif chosen_option == "Відео про прикладну математику":
            await step_context.context.send_activity(MessageFactory.text("https://www.youtube.com/watch?v=azu_tI9wrWA"))

        elif chosen_option == "День відкритих дверей":
            reply.attachments.append(self.open_door_card())
            reply.text = "https://www.youtube.com/watch?v=yJnWV-N0Od8"
            await step_context.context.send_activity(reply)

        elif chosen_option == "Презентація":
            await step_context.context.send_activity(MessageFactory.text("http://amath.lp.edu.ua/wp-content/uploads/pm-study.pdf"))

        elif chosen_option == "Навчальні дисципліни":
            await step_context.context.send_activity(MessageFactory.text("http://amath.lp.edu.ua/for-students-old/modules-description/"))

        elif chosen_option == "Соцмережі і сайти":
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Офіційна сторінка кафедри: http://amath.lp.edu.ua/\n\n"
                    f"Telegram-канал: https://t.me/amath_lp_edu_ua\n\n"
                    f"Група у Facebook: https://www.facebook.com/groups/amath.lp\n\n"
                    f"Wiki-сторінка: http://wiki.lp.edu.ua/wiki/%D0%9A%D0%B0%D1%84%D0%B5%D0%B4%D1%80%D0%B0_%D0%BF%D1%80%D0%B8%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%BE%D1%97_%D0%BC%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B8"
                )
            )

        elif chosen_option == "Контакти":
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Адреса: вул. Митрополита Андрея 5, 4-й н.к., кім. 213\n\n"
                    f"E-mail: pm.dept@lpnu.ua\n\n"
                    f"Номер телефону: (032) 258-23-68"
                )
            )
        elif chosen_option == "Навчальні лабораторії":
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Навчальна лабораторія знаходиться за адресою: 4й навчальний корпус, 225 ауд.\n\n"
                    f"Навчальна лабораторія містить три комп’ютерні класи, кожен із яких обладнаний сучасною технікою та усім необхідним для навчання студентів програмним забезпеченням.\n\n"
                    f"Кафедра прикладної математики бере участь у програмі MSDN Academic Alliance, яка дає доступ до широкого переліку сучасних продуктів Microsoft для освітніх та навчальних цілей:\n\n"
                    f" усе програмне забезпечення MSDN AA безкоштовно доступне для всіх студентів, аспірантів та викладачів кафедри для некомерційного використання з навчальними, науковими та дослідницькими цілями;\n\n"
                    f" усе програмне забезпечення можна встановлювати на будь-яку кількість комп`ютерів в навчальних классах та лабораторіях кафедри;\n\n"
                    f" викладачі, співробітники і студенти кафедри можуть встановлювати отримане в рамках MSDN AA програмне забезпечення на своїх особистих ПК."
                )
            )

        return await step_context.replace_dialog(
            ReviewKafedra.__name__
        )

    def video_card1(self) -> Attachment:
        return Attachment(
            name="YoutubeVideo",
            content_type="video/mp4",
            content_url="http://amath.lp.edu.ua/wp-content/uploads/amath-2018-1.mp4",
        )

    def open_door_card(self) -> Attachment:
        card = HeroCard(
            title="",
            images=[
                CardImage(
                    url="http://amath.lp.edu.ua/wp-content/uploads/feed-open-day-2021-04-17-v2.jpg"
                )
            ],
        )
        return CardFactory.hero_card(card)
