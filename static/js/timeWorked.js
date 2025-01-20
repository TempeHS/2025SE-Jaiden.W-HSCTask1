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

    const startTimeInput = document.getElementById("start_time");
    const endTimeInput = document.getElementById("end_time");

    startTimeInput.addEventListener("change", calculateTimeWorked);
    endTimeInput.addEventListener("change", calculateTimeWorked);

    // Set initial values to the current time rounded to the nearest 15 minutes
    const now = new Date();
    const roundedNow = roundToNearest15(new Date(now));
    const formattedDateTime = formatDateToLocalISO(roundedNow);
    startTimeInput.value = formattedDateTime;
    endTimeInput.value = formattedDateTime;
    calculateTimeWorked();
});
