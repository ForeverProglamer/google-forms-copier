headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    'Accept': '*/*'
}

classes = {
    'is_checked': 'isChecked',
    'is_selected': 'isSelected'
}

selectors = {
    'src': {
        'question_element': '.freebirdFormviewerViewNumberedItemContainer > .freebirdFormviewerViewItemsItemItem',
        'question_title': '.freebirdFormviewerViewItemsItemItemTitle.exportItemTitle.freebirdCustomFont',
        'radiobutton_option': '.freebirdFormviewerViewItemsRadioOptionContainer > label',
        'radiobutton_label': '.freebirdFormviewerViewItemsRadioLabel',
        'checkbox_option': 'label.freebirdFormviewerViewItemsCheckboxContainer',
        'checkbox_label': '.freebirdFormviewerViewItemsCheckboxLabel',
        'text_label': '.freebirdFormviewerViewItemsTextTextItemContainer > div',
        'select_option': '.quantumWizMenuPaperselectOption',
        'select_label': 'span'
    },

    'dest': {
        'question_element': '.freebirdFormviewerViewNumberedItemContainer div.m2',
        'general_div': 'div[jscontroller="sWGJ4b"] div[jscontroller]',
        'question_title': '.freebirdFormviewerComponentsQuestionBaseTitle',
        'radiobutton_option': '.freebirdFormviewerComponentsQuestionRadioChoice > label',
        'radiobutton_label': '.freebirdFormviewerComponentsQuestionRadioLabel',
        'checkbox_option': 'label.docssharedWizToggleLabeledContainer.freebirdFormviewerComponentsQuestionCheckboxCheckbox',
        'select': '.quantumWizMenuPaperselectOptionList',
        'select_option': 'div[jsname="V68bde"] .quantumWizMenuPaperselectOption',
        'select_label': 'span',
        'short_text': 'input',
        'long_text': 'textarea'
    }
}

jscontrollers = {
    'src': {
        'text': 'rDGJeb',
        'radiobutton': 'pkFYWb',
        'checkbox': 'hIYTQc',
        'select': 'jmDACb'
    },

    'dest': {
        'text': 'oCiKKc',
        'radiobutton': 'UmOCme',
        'checkbox': 'sW52Ae',
        'select': 'liFoG'
    }
}