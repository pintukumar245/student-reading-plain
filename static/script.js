const courseStreams = window.courseStreamsData;
const subjects = window.subjectsData;

document.addEventListener("DOMContentLoaded", function () {
    const classYearSelect = document.getElementById("classYear");
    const courseStreamSelect = document.getElementById("courseStream");
    const subjectSelect = document.getElementById("subject");

    classYearSelect.addEventListener("change", function () {
        const classYear = this.value;
        courseStreamSelect.innerHTML = '<option value="" disabled selected>Choose Course Stream</option>';

        if (courseStreams[classYear]) {
            courseStreams[classYear].forEach(stream => {
                let option = document.createElement("option");
                option.value = stream;
                option.text = stream;
                courseStreamSelect.add(option);
            });
        }

        subjectSelect.innerHTML = '<option value="" disabled selected>Choose Subject</option>';
    });

    courseStreamSelect.addEventListener("change", function () {
        const courseStream = this.value;
        subjectSelect.innerHTML = '<option value="" disabled selected>Choose Subject</option>';

        if (subjects[courseStream]) {
            subjects[courseStream].forEach(sub => {
                let option = document.createElement("option");
                option.value = sub;
                option.text = sub;
                subjectSelect.add(option);
            });
        }
    });
});