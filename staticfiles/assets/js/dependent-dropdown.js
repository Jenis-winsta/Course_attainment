window.onload = function () {
    const selectYear = document.getElementById('year');
    const selectSemester = document.getElementById('semester');
    const selectCourse = document.getElementById('course');

    // Fetch years from backend
    fetch('/get_years/')
        .then(response => response.json())
        .then(years => {
            years.forEach(year => {
                selectYear.options[selectYear.options.length] = new Option(year.name, year.id);
            });
        });

    // Event listener for year change
    selectYear.onchange = function () {
        const yearId = selectYear.value;

        // Fetch semesters for the selected year
        fetch(`/get_semesters/${yearId}/`)
            .then(response => response.json())
            .then(data => {
                selectSemester.innerHTML = '<option value="">Select Semester</option>';
                data.forEach(semester => {
                    selectSemester.innerHTML += `<option value="${semester.id}">${semester.name}</option>`;
                });
            });
    };

    // Event listener for semester change
    selectSemester.onchange = function () {
        const semesterId = selectSemester.value;

        // Fetch courses for the selected semester
        fetch(`/get_courses/${semesterId}/`)
            .then(response => response.json())
            .then(data => {
                selectCourse.innerHTML = '<option value="">Select Course</option>';
                data.forEach(course => {
                    selectCourse.innerHTML += `<option value="${course.id}">${course.name}</option>`;
                });
            });
    };
};
