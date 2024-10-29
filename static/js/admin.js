// Function to add information
function addInformation() {
    const infoText = document.getElementById('info-text');
    const newInfo = prompt('Enter new information:');
    if (newInfo) {
      infoText.innerHTML += `<br>${newInfo}`;
    }
  }
  
  // Function to update information
  function updateInformation() {
    const infoText = document.getElementById('info-text');
    const updatedInfo = prompt('Update the information:');
    if (updatedInfo) {
      infoText.innerHTML = updatedInfo;
    }
  }
  
  // Function to edit information
  // function editInformation() {
  //   const infoText = document.getElementById('info-text');
  //   const currentInfo = infoText.innerHTML;
  //   const editedInfo = prompt('Edit the current information:', currentInfo);
  //   if (editedInfo) {
  //     infoText.innerHTML = editedInfo;
  //   }
  // }

  // edit file
  function toggleFileEditor() {
    var editorSection = document.getElementById("fileEditorSection");
    if (editorSection.style.display === "none") {
        editorSection.style.display = "block";
        // Load the current file content via AJAX
        fetch('/edit_sample')
            .then(response => response.text())
            .then(data => {
                document.getElementById('file-content').value = data;
            })
            .catch(error => console.error('Error loading file content:', error));
    } else {
        editorSection.style.display = "none";
    }
    // document.getElementById("fileEditorSection").style.display = "none";
}