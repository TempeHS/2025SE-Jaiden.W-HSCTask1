document.addEventListener("DOMContentLoaded", function() {
    function roundToNearest15(date) {
        const minutes = Math.ceil(date.getMinutes() / 15) * 15;
        date.setMinutes(minutes);
        date.setSeconds(0);
        date.setMilliseconds(0);
        return date;
    }

    function calculateTimeWorked() {
        const startTime = new Date(document.getElementById("start_time").value);
        const endTime = new Date(document.getElementById("end_time").value);
        if (startTime && endTime) {
            let timeWorked = (endTime - startTime) / (1000 * 60); // time worked in minutes
            timeWorked = Math.ceil(timeWorked / 15) * 15; // round up to nearest 15 minutes
            const hoursWorked = timeWorked / 60; // convert to hours
            document.getElementById("time_worked").value = hoursWorked.toFixed(2);
        }
    }

    function formatDateToLocalISO(date) {
        const tzOffset = date.getTimezoneOffset() * 60000; // offset in milliseconds
        const localISOTime = new Date(date - tzOffset).toISOString().slice(0, -1);
        return localISOTime;
    }

    const startTimeInput = document.getElementById("start_time");
    const endTimeInput = document.getElementById("end_time");

    startTimeInput.addEventListener("change", function() {
        const startTime = new Date(startTimeInput.value);
        startTimeInput.value = formatDateToLocalISO(startTime);
        calculateTimeWorked();
    });

    endTimeInput.addEventListener("change", function() {
        const endTime = new Date(endTimeInput.value);
        endTimeInput.value = formatDateToLocalISO(endTime);
        calculateTimeWorked();
    });

    // Set initial values to the current time rounded to the nearest 15 minutes
    const now = new Date();
    const roundedNow = roundToNearest15(new Date(now));
    const formattedDateTime = formatDateToLocalISO(roundedNow);
    startTimeInput.value = formattedDateTime;
    endTimeInput.value = formattedDateTime;
    calculateTimeWorked();
});
