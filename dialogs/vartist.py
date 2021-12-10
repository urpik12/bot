import re
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


class ReviewVartist(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(ReviewVartist, self).__init__(
            dialog_id or ReviewVartist.__name__
        )

        self.COMPANIES_SELECTED = "value-companiesSelected"
        self.DONE_OPTION = "done"


        self.list_of_choices = [
            Choice('Денна форма'),
            Choice('Заочна форма'),
            Choice('Назад'),
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
            prompt=MessageFactory.text("Підменю Вартість"),
            # retry_prompt=MessageFactory.text(""),
            choices=self.list_of_choices,
            style=ListStyle.hero_card,
        )
        return await step_context.prompt(ChoicePrompt.__name__, prompt_options)


    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        chosen_option = step_context.result.value
        
        reply = MessageFactory.list([])
        test_reply_for_skype = MessageFactory.list([])

        if chosen_option == "Назад":
            return await step_context.end_dialog()

        # ======================================
        # Зараз в скайпі не можна загружати pdf
        # як дізнатися що клієнт в скайпі не знаю
        # якщо трай не працює то це скайп і треба ссилки
        # ======================================
        elif chosen_option == "Денна форма":
            try:
                test_reply_for_skype.attachments.append(self.vartist_denna())
                await step_context.context.send_activity(test_reply_for_skype)
            except:
                reply.attachments.append(self.vartist_denna_card())
                await step_context.context.send_activity(reply)
        elif chosen_option == "Заочна форма":
            try:
                test_reply_for_skype.attachments.append(self.vartist_zaochna())
                await step_context.context.send_activity(test_reply_for_skype)
            except:
                reply.attachments.append(self.vartist_zaochna_card())
                await step_context.context.send_activity(reply)
        

        
        return await step_context.replace_dialog(
            ReviewVartist.__name__
        )
        

        
    def vartist_denna(self) -> Attachment:
        return Attachment(
            name="vartist-2021-denna.pdf",
            content_type="application/pdf",
            content_url="https://lpnu.ua/sites/default/files/2020/pages/3812/vartist-2021-denna.pdf",
        )

    def vartist_denna_card(self) -> Attachment:
        card = HeroCard(
            title="",
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="open url",
                    value="https://lpnu.ua/sites/default/files/2020/pages/3812/vartist-2021-denna.pdf",
                )
            ],
        )
        return CardFactory.hero_card(card)

    
    def vartist_zaochna(self) -> Attachment:
        return Attachment(
            name="vartist-zaochna-2021.pdf",
            content_type="application/pdf",
            content_url="https://lpnu.ua/sites/default/files/2020/pages/3812/vartist-zaochna-2021.pdf",
        )

    def vartist_zaochna_card(self) -> Attachment:
        card = HeroCard(
            title="",
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="open url",
                    value="https://lpnu.ua/sites/default/files/2020/pages/3812/vartist-zaochna-2021.pdf",
                )
            ],
        )
        return CardFactory.hero_card(card)