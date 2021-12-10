import re, os, base64
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
    Activity,
    ActivityTypes,
    ActionTypes,
    Attachment,
    AnimationCard,
    AudioCard,
    HeroCard,
    OAuthCard,
    VideoCard,
    ReceiptCard,
    SigninCard,
    ThumbnailCard,
    MediaUrl,
    CardAction,
    CardImage,
    ThumbnailUrl,
    Fact,
    ReceiptItem,
    AttachmentLayoutTypes,
)



class ReviewZno(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(ReviewZno, self).__init__(
            dialog_id or ReviewZno.__name__
        )

        self.COMPANIES_SELECTED = "value-companiesSelected"
        self.DONE_OPTION = "done"


        self.list_of_choices = [
            Choice('Узагальнена статистика'), # http://amath.lp.edu.ua/wp-content/uploads/appMath.pdf
            Choice('Статистика від osvita.ua'), # 
            Choice('Рейтингові списки 2021'), #             
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
            prompt=MessageFactory.text("Підменю Ймовірність вступу"),
            # retry_prompt=MessageFactory.text("Please choose an option from the list"),
            choices=self.list_of_choices,
            style=ListStyle.hero_card
        )
        return await step_context.prompt(ChoicePrompt.__name__, prompt_options)


    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        chosen_option = step_context.result.value
        
        reply = MessageFactory.list([])
        test_reply_for_skype = MessageFactory.list([])

        if chosen_option == "Назад":
            return await step_context.end_dialog()
        elif chosen_option == "Узагальнена статистика":
            reply.attachments.append(self.get_stat_photo_attachment())
            await step_context.context.send_activity(reply)
        elif chosen_option == "Статистика від osvita.ua":
            await step_context.context.send_activity(MessageFactory.text("https://vstup.osvita.ua/y2020/r14/97/"))
        elif chosen_option == "Рейтингові списки 2021":
            await step_context.context.send_activity(MessageFactory.text("https://vstup.lpnu.ua/detail/5/19773/8/1"))

        return await step_context.replace_dialog(
            ReviewZno.__name__
        )
        

    def get_stat_photo_attachment(self) -> Attachment:
        file_path = os.path.join(os.getcwd(), "resources/stats.jpg")
        with open(file_path, "rb") as in_file:
            base64_image = base64.b64encode(in_file.read()).decode()

        return Attachment(
            name="Узагальнена статистика",
            content_type="image/jpg",
            content_url=f"data:image/png;base64,{base64_image}",
        )