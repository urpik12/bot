import os, base64
from typing import List


from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ComponentDialog,
)
from botbuilder.dialogs.choices.list_style import ListStyle
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions
from botbuilder.dialogs.choices import Choice, FoundChoice
from botbuilder.core import CardFactory, MessageFactory

from botbuilder.schema import (
    Attachment
)



class ReviewVstup(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(ReviewVstup, self).__init__(
            dialog_id or ReviewVstup.__name__
        )

        self.COMPANIES_SELECTED = "value-companiesSelected"
        self.DONE_OPTION = "done"


        self.list_of_choices = [
            Choice("Документи для вступу"),
            Choice("Терміни подачі заяв"),
            Choice("Конкурсні предмети"),
            Choice("Пільги"),
            Choice("Назад"),
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
            prompt=MessageFactory.text("Підменю вступ"),
            # retry_prompt=MessageFactory.text("Please choose an option from the list"),
            choices=self.list_of_choices,
            style=ListStyle.hero_card
        )
        return await step_context.prompt(ChoicePrompt.__name__, prompt_options)


    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        chosen_option = step_context.result.value
        
        reply = MessageFactory.list([])

        if chosen_option == "Назад":
            return await step_context.end_dialog()
        elif chosen_option == "Документи для вступу":
            reply.attachments.append(self.get_stat_photo_attachment())
            await step_context.context.send_activity(reply)
        elif chosen_option == "Терміни подачі заяв":
            await step_context.context.send_activity(MessageFactory.text("https://lpnu.ua/sites/default/files/2020/pages/3792/termin-pzso2v.pdf"))
        elif chosen_option == "Конкурсні предмети":
            await step_context.context.send_activity(MessageFactory.text("https://lpnu.ua/sites/default/files/2020/pages/3793/znom2021-1301.pdf"))        
        elif chosen_option == "Пільги":
            await step_context.context.send_activity(MessageFactory.text("https://mon.gov.ua/storage/app/media/vishcha-osvita/vstup-2021/informaciya.shodo.pilg.2021/Dodatok.lyst.1.9-311_14.06.2021.pdf"))

        return await step_context.replace_dialog(
            ReviewVstup.__name__
        )
        

    def get_stat_photo_attachment(self) -> Attachment:
        file_path = os.path.join(os.getcwd(), "resources/vstup_docs.jpg")
        with open(file_path, "rb") as in_file:
            base64_image = base64.b64encode(in_file.read()).decode()

        return Attachment(
            name="Список необхідних документів для вступу",
            content_type="image/jpg",
            content_url=f"data:image/png;base64,{base64_image}",
        )
