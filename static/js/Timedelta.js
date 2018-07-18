
function Timedelta(distance) {
    // Class Timedelta can calculate the days, hours, minutes and seconds from the given distance in milliseconds
    
    this.distance = distance;
    
    this.getDays = function() {
        return Math.floor(this.distance / (1000 * 60 * 60 * 24));
    }
    
    this.getHours = function() {
        return Math.floor((this.distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    }
    
    this.getMinutes = function() {
        return Math.floor((this.distance % (1000 * 60 * 60)) / (1000 * 60));
    }
    
    this.getSeconds = function() {
        return Math.floor((this.distance % (1000 * 60)) / 1000);
    }
    
    this.toString = function(type) {
        if (type === undefined) {
            type = "condensed";
        }
        if (type == "condensed") {
            return this.getDays() + "d " + 
                   pad(this.getHours(), 2) + ":" + 
                   pad(this.getMinutes(), 2) + ":" + 
                   pad(this.getSeconds(), 2); 
        } else {
            return this.getDays() + "d " + 
                   this.getHours() + "h " + 
                   this.getMinutes() + "m " + 
                   this.getSeconds() + "s";
        }
    }
}

function pad(number, length) {
    var str = '' + number;
    while (str.length < length) {
        str = '0' + str;
    }
    return str;

}