// Get references to elements 
const textarea1 = document.getElementById('textarea1');
const textarea2 = document.getElementById('textarea2');
const textarea3 = document.getElementById('textarea3');
const wrapper1 = document.getElementById('textarea-wrapper-1');
const wrapper2 = document.getElementById('textarea-wrapper-2');
const wrapper3 = document.getElementById('textarea-wrapper-3');
const submitBtn = document.getElementById('submitBtn');


 // When the icon is clicked, toggle the description display
 document.getElementById('infoIcon').addEventListener('click', function() {
  var description = document.getElementById('description');
  if (description.style.display === "none" || description.style.display === "") {
    description.style.display = "block";
  } else {
    description.style.display = "none";
  }
});

// Function to update placeholder visibility
function updatePlaceholder(wrapper, textarea) {
  if (textarea.value.trim().length > 0) {
    wrapper.classList.add('not-empty');
  } else {
    wrapper.classList.remove('not-empty');
  }
}

// Event Listeners for Field 1
textarea1.addEventListener('focus', () => {
  wrapper1.classList.add('focused');
});
textarea1.addEventListener('blur', () => {
  wrapper1.classList.remove('focused');
  updatePlaceholder(wrapper1, textarea1);
});
textarea1.addEventListener('input', () => {
  updatePlaceholder(wrapper1, textarea1);
  checkButtonState();
});

// Event Listeners for Field 2
textarea2.addEventListener('focus', () => {
  wrapper2.classList.add('focused');
});
textarea2.addEventListener('blur', () => {
  wrapper2.classList.remove('focused');
  updatePlaceholder(wrapper2, textarea2);
});
textarea2.addEventListener('input', () => {
  updatePlaceholder(wrapper2, textarea2);
  checkButtonState();
});

// Event Listeners for Field 3
textarea3.addEventListener('focus', () => {
  wrapper3.classList.add('focused');
});
textarea3.addEventListener('blur', () => {
  wrapper3.classList.remove('focused');
  updatePlaceholder(wrapper3, textarea3);
});
textarea3.addEventListener('input', () => {
  updatePlaceholder(wrapper3, textarea3);
  checkButtonState();
});

// Enable the submit button only when both textareas have non-empty content
function checkButtonState() {
  if (textarea1.value.trim() !== "" && textarea2.value.trim() !== "") {
    submitBtn.disabled = false;
    submitBtn.classList.add('enabled');
  } else {
    submitBtn.disabled = true;
    submitBtn.classList.remove('enabled');
  }
}






/*

// File input trigger inside Field 1
const fileTrigger = document.getElementById('file-trigger');
const hiddenFileInput = document.getElementById('hiddenFileInput');

fileTrigger.addEventListener('click', (e) => {
  e.stopPropagation();
  hiddenFileInput.click();
});


hiddenFileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file && file.name.endsWith(".docx")) {
    const reader = new FileReader();
    reader.onload = function(evt) {
      const arrayBuffer = evt.target.result;
      mammoth.extractRawText({ arrayBuffer: arrayBuffer })
        .then(function(result) {
          textarea1.value = result.value;
          updatePlaceholder(wrapper1, textarea1);
          checkButtonState();
        })
        .catch(function(err) {
          console.error("Error extracting text from DOCX:", err);
        });
    };
    reader.readAsArrayBuffer(file);
  } else if (file) {
    const reader = new FileReader();
    reader.onload = function(evt) {
      textarea1.value = evt.target.result;
      updatePlaceholder(wrapper1, textarea1);
      checkButtonState();
    };
    reader.readAsText(file);
  }
});

*/










// File input trigger inside Field 1
const fileTrigger = document.getElementById('file-trigger');
const hiddenFileInput = document.getElementById('hiddenFileInput');

fileTrigger.addEventListener('click', (e) => {
  e.stopPropagation();
  hiddenFileInput.click();
});

hiddenFileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    if (file.name.endsWith(".docx")) {
      // Handle DOCX using Mammoth
      const reader = new FileReader();
      reader.onload = function(evt) {
        const arrayBuffer = evt.target.result;
        mammoth.extractRawText({ arrayBuffer: arrayBuffer })
          .then(function(result) {
            textarea1.value = result.value;
            updatePlaceholder(wrapper1, textarea1);
            checkButtonState();
          })
          .catch(function(err) {
            console.error("Error extracting text from DOCX:", err);
          });
      };
      reader.readAsArrayBuffer(file);
    } else if (file.name.endsWith(".pdf")) {
      // Handle PDF using pdf.js
      const reader = new FileReader();
      reader.onload = function(evt) {
        const arrayBuffer = evt.target.result;
        // Load the PDF document from the array buffer
        const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
        loadingTask.promise.then(pdf => {
          let maxPages = pdf.numPages;
          let countPromises = []; // Array to hold promises for each page's text
          for (let i = 1; i <= maxPages; i++) {
            let pagePromise = pdf.getPage(i).then(page => {
              return page.getTextContent().then(textContent => {
                let textItems = textContent.items;
                let finalString = "";
                for (let j = 0; j < textItems.length; j++) {
                  finalString += textItems[j].str + " ";
                }
                return finalString;
              });
            });
            countPromises.push(pagePromise);
          }
          // Wait for all pages and join their text
          Promise.all(countPromises).then(texts => {
            const fullText = texts.join("\n\n");
            textarea1.value = fullText;
            updatePlaceholder(wrapper1, textarea1);
            checkButtonState();
          });
        }, function (reason) {
          console.error("Error extracting text from PDF:", reason);
        });
      };
      reader.readAsArrayBuffer(file);
    } else {
      // Fallback: read as text for other file types
      const reader = new FileReader();
      reader.onload = function(evt) {
        textarea1.value = evt.target.result;
        updatePlaceholder(wrapper1, textarea1);
        checkButtonState();
      };
      reader.readAsText(file);
    }
  }
});














// Allow clicking anywhere in the textarea wrapper to focus the textarea
wrapper1.addEventListener('click', () => {
  textarea1.focus();
});
wrapper2.addEventListener('click', () => {
  textarea2.focus();
});
wrapper3.addEventListener('click', () => {
  textarea3.focus();
});

// Submit button action
submitBtn.addEventListener('click', async () => {
  // Store original button text
  const originalText = submitBtn.textContent;
  
  // Disable button and start a cooldown countdown
  submitBtn.disabled = true;
  submitBtn.classList.remove('enabled');
  let timeLeft = 5;

  const countdown = setInterval(() => {
    submitBtn.textContent = `${timeLeft}s`;
    timeLeft--;

    if (timeLeft < 0) {
      clearInterval(countdown);
      submitBtn.textContent = originalText;
      // Optionally, re-enable the button after the countdown
      submitBtn.disabled = false;     
      submitBtn.classList.add('enabled');
    }
  }, 1000);

  // Get values from textareas
  const field1Text = textarea1.value;
  const field2Text = textarea2.value;
  const field3Text = textarea3.value;

  // Prepare form data to send to Flask
  const formData = new FormData();
  formData.append('field1', field1Text);
  formData.append('field2', field2Text);
  formData.append('field3', field3Text);

  try {
    // Send data to the Flask endpoint
    const response = await fetch('/cover-letter/submit', {
      method: 'POST',
      body: formData
    });

    // Convert the response to JSON
    const data = await response.json();
    console.log("Response from Flask:", data);

    // Display the returned result in a modal popup
    // Assumes your Flask response returns JSON with a key "result"
    const resultTextElem = document.getElementById('resultText');
    const popupModal = document.getElementById('popupModal');
    
    resultTextElem.textContent = data.result;
    popupModal.style.display = 'block';

  } catch (error) {
    console.error("Error:", error);
  }
});


document.getElementById('closeModal').addEventListener('click', function() {
  document.getElementById('popupModal').style.display = 'none';
});
