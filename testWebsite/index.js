// Declare codeList array
let codeList = [];

function populateBlocks() {
    fetch('http://localhost:5000/getBlocks',)
    .then(response => {
        if (response.ok) {
            return response.text();  // Or handle JSON if needed
        } else {
            throw new Error('Network response for BLOCKS was not ok.');
        }
    })
    .then(data => {
        // Display the returned JSON data
        document.getElementById('result').innerHTML = `
            <h2>Submission Result:</h2>
            <pre>${JSON.stringify(data, null, 2)}</pre>
        `;            })
    .catch(error => {
        document.getElementById('result').innerText = 'Error: ' + error.message;
    });
}

populateBlocks();

// Optional: Add JavaScript if you want to handle the response dynamically without reloading the page
document.getElementById('courseForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Prevent the default form submission

    const formData = new FormData(this);

    fetch('http://localhost:5000/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.text();  // Or handle JSON if needed
        } else {
            throw new Error('Network response for SUBMIT CODES was not ok.');
        }
    })
    .then(data => {
        // Display the returned JSON data
        document.getElementById('result').innerHTML = `
            <h2>Submission Result:</h2>
            <pre>${JSON.stringify(data, null, 2)}</pre>
        `;            })
    .catch(error => {
        document.getElementById('result').innerText = 'Error: ' + error.message;
    });
});

// Function to add course code to the list
function addCourse() {
    const codeBox = document.getElementById("course_code");
    const courseCode = codeBox.value.trim();  // Trim the input value

    if (courseCode !== "") {
        // Push the code to the codeList array
        codeList.push(courseCode);

        // Create a new li element and set its content
        const newListItem = document.createElement("li");
        newListItem.textContent = courseCode;

        // Append the new li element to the ul with id 'codeList'
        document.getElementById("codeList").appendChild(newListItem); // Use the correct ID

        // Clear the input box after adding the course
        codeBox.value = "";
    }
}

// Handle the 'Add Course' button click
document.getElementById('addCourse').addEventListener('click', addCourse);

// Handle the Enter key press inside the course_code input field
document.getElementById('course_code').addEventListener('keydown', function(event) {
    if (event.key === "Enter") {  // Check if Enter key was pressed
        event.preventDefault();    // Prevent form submission
        addCourse();               // Call the function to add course
    }
});
