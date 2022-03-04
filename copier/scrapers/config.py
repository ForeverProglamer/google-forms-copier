headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    'Accept': '*/*'
}

classes = {
    'is_checked': 'N2RpBe',
}

selectors = {
    'src': {
        'question_element': 'div[role="listitem"] > div[jscontroller]',
        'question_title': 'div[role="heading"]',
        'radiobutton_option': '.docssharedWizToggleLabeledContainer',
        'radiobutton_label': 'span',
        'checkbox_option': '.ujnDW',
        'checkbox_checked_option': 'div[aria-checked="true"]',
        'checkbox_label': '.aDTYNe.snByac.gjE2o',
        'text_label': '.Mh5jwe.JqSWld.yqQS1',
        'long_text_label': '.q4tvle.JqSWld.yqQS1',
        'select_option': 'div[jsname="wQNmvb"]',
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