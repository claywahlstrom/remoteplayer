
function Timedelta(distance) {
    // Class Timedelta can calculate the days, hours, minutes and seconds from the given distance in milliseconds
    if (distance === undefined) {
        throw "expected distance parameter but none found";
    }
    this.distance = distance;
}

Timedelta.prototype.getDays = function() {
    return Math.floor(this.distance / (1000 * 60 * 60 * 24));
};

Timedelta.prototype.getHours = function() {
    return Math.floor((this.distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
};

Timedelta.prototype.getMinutes = function() {
    return Math.floor((this.distance % (1000 * 60 * 60)) / (1000 * 60));
};

Timedelta.prototype.getPercentage = function (startTime, digitsToRound) {
    if (startTime === undefined || typeof startTime !== "number") {
        throw "expected a start date of type Date";
    }
    if (digitsToRound === undefined) {
        digitsToRound = 2
    }
    var td = new Timedelta(new Date().getTime() - startTime);
    var percentage = td.distance / (td.distance + this.distance) * 100
    return Math.round(percentage * Math.pow(10, digitsToRound)) / Math.pow(10, digitsToRound);
};

Timedelta.prototype.getSeconds = function() {
    return Math.floor((this.distance % (1000 * 60)) / 1000);
};

Timedelta.prototype.toString = function(type) {
    if (type === undefined ||
        (type !== "labeled" && type !== "standard")) {
        return "must enter either labeled or standard";
    }
    if (type == "standard") {
        return this.getDays() + "d " +
            this.getPadded(this.getHours(), 2) + ":" +
            this.getPadded(this.getMinutes(), 2) + ":" +
            this.getPadded(this.getSeconds(), 2);
    } else {
        return this.getDays() + "d " +
            this.getHours() + "h " +
            this.getMinutes() + "m " +
            this.getSeconds() + "s";
    }
};

Timedelta.prototype.getPadded = function(number, length) {
    var str = '' + number;
    while (str.length < length) {
        str = '0' + str;
    }
    return str;

};

function dateGe(date, otherDate) {
    return date >= otherDate
        || (date.getFullYear() === otherDate.getFullYear()
        && date.getMonth() === otherDate.getMonth()
        && date.getDate() === otherDate.getDate());
}