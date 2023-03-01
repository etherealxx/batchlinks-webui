let prevTextAreaValue = '';
let isTextAreaVisible = true;

onUiUpdate(function() {
    const textArea = gradioApp().querySelectorAll('#tab_batchlinks textarea')?.[2];
    const textAreaValue = textArea ? textArea.value : '';

    if (isTextAreaVisible && textAreaValue.startsWith('All done!') && prevTextAreaValue !== textAreaValue) {
        gradioApp().querySelector('#finish_audio audio')?.play();
    }

    if (!textArea) {
        isTextAreaVisible = false;
    } else if (textArea.style.display !== 'none') {
        isTextAreaVisible = true;
    }

    prevTextAreaValue = textAreaValue;
});
