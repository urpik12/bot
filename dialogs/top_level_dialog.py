from re import M
from botbuilder.core import MessageFactory
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
)
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.choices.list_style import ListStyle

from dialogs.vartist import ReviewVartist
from dialogs.vstup import ReviewVstup
from dialogs.kafedra import ReviewKafedra
from dialogs.zno import ReviewZno

from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions
from botbuilder.dialogs.choices import Choice, FoundChoice, choice


class TopLevelDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(TopLevelDialog, self).__init__(
            dialog_id or TopLevelDialog.__name__)

        self.USER_INFO = "value-userInfo"

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ReviewVstup(ReviewVstup.__name__))
        self.add_dialog(ReviewKafedra(ReviewKafedra.__name__))
        self.add_dialog(ReviewVartist(ReviewVartist.__name__))
        self.add_dialog(ReviewZno(ReviewZno.__name__))

        self.add_dialog(
            WaterfallDialog(
                "dialog",
                [
                    self.show_menu,
                    self.open_submenu,
                    self.loop_menu,
                ],
            )
        )

        self.initial_dialog_id = "dialog"

    async def show_menu(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        list_of_choices = [
            Choice('Про кафедру'),
            Choice('Вступ'),
            Choice('Ймовірність вступу'),
            Choice('Вартість навчання'),
        ]

        return await step_context.prompt((ChoicePrompt.__name__),
                                         PromptOptions(prompt=MessageFactory.text("\n\n\n\nГоловне меню"),
                                                       style=ListStyle.hero_card,
                                                       # style=ListStyle.suggested_action,
                                                       choices=list_of_choices))

    async def open_submenu(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        chosen_option = step_context.result.value
        if chosen_option == "Вартість навчання":
            return await step_context.begin_dialog(ReviewVartist.__name__)
        elif chosen_option == "Вступ":
            return await step_context.begin_dialog(ReviewVstup.__name__)
        elif chosen_option == "Про кафедру":
            return await step_context.begin_dialog(ReviewKafedra.__name__)
        elif chosen_option == "Ймовірність вступу":
            return await step_context.begin_dialog(ReviewZno.__name__)

    async def loop_menu(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        return await step_context.replace_dialog(
            TopLevelDialog.__name__
        )
