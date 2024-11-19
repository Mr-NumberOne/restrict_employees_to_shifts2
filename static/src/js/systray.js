/* @odoo-module */
import { Component } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc_service";
import { registry } from "@web/core/registry";
const { onMounted, onWillUnmount } = owl;

class TimerSystrayItem extends Component {
    static template = "restrict_employees_to_shifts.TimerSystray";

    setup() {
        super.setup();
        this.shiftInterval = null;
        this.requestInterval = null;
        this.requestInMinutes = 1;
        this.minutes = 0;
        this.getIdleTime();
    }

    async getIdleTime() {
        try {
            const data = await jsonrpc('/hr/shift_restricted', { method: 'call' });
            if (data) {
                this.minutes = data;
                document.querySelector("#div-timer").style.display = "flex";
                this.startIdleTimer();
            }else{
                document.querySelector("#div-timer").style.display = "none";
            }
        } catch (error) {
            console.error("Failed to get remaining time:", error);
        }
    }

    startIdleTimer() {
        const updateTimer = () => {
            const now = new Date().getTime();
            const date = new Date(now);
            date.setMinutes(date.getMinutes() + this.minutes);
            this.updatedTimestamp = date.getTime();
        };

        updateTimer(); // Initial update

        const resetTimer = () => {
            updateTimer();
            this.updateDisplay();
        };

        this.shiftInterval = setInterval(() => {
            const now = new Date().getTime();
            const distance = this.updatedTimestamp - now;

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            if (distance < 0) {
                clearInterval(this.shiftInterval);
                clearInterval(this.requestInterval);
                document.querySelector("#idle_timer").innerHTML = "EXPIRED";
                location.replace("/web/session/logout");
            } else {
                this.updateDisplay(days, hours, minutes, seconds);
            }
        }, 1000);
        this.requestInterval = setInterval(()=>{
            document.querySelector("#idle_timer").style.visibility = "none"
            this.getIdleTime()
        },1000 * 60 * this.requestInMinutes)
    };

    updateDisplay(days, hours, minutes, seconds) {
        let display = "";
        if (days) display += days + "d ";
        if (hours) display += hours + "h ";
        display += minutes + "m " + seconds + "s ";
        document.querySelector("#idle_timer").innerHTML = display;
    }

    onWillUnmount() {
        if (this.shiftInterval) {
            clearInterval(this.shiftInterval);
        }
        if (this.requestInterval) {
            clearInterval(this.requestInterval);
        }
    }
}

export const systrayItem = {
    Component: TimerSystrayItem
};
registry.category("systray").add("restrict_employees_to_shifts.TimerSystray", systrayItem, { sequence: 25 });
