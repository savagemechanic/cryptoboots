
var pyvars = {
    plans: plans,
    selected_plans: [],
    total_earning: 0.00,
    amount: 0.00,
    days: 0,
    error: null,
}

// Object.freeze(pyvars)

const calculate_earnings = new Vue({
    el: '#calculate_earnings',
    data () {
        return pyvars
    },
    computed: {
        least_deposit() {
            min_deposits = this.plans.map(function (plan) {
                return plan.minimum_deposit
            })
            return Math.min(...min_deposits)
        },
    },
    watch : {
        'days': function(newValue, oldValue) {
            this.calculate_earnings()
        },
        'amount': function(newValue, oldValue) {
            this.calculate_earnings()
        },
        'selected_plans': function(newValue, oldValue) {
            this.calculate_earnings()
        }
    },
    methods: {
        calculate_earnings() {
            var selected_plan_ids = this.selected_plans
            if (selected_plan_ids) {
                // turn selected ids to objects
                var selected_plans = []
                for (var plan_id of selected_plan_ids) {
                    selected_plans.push(this.get_plan_by_id(parseInt(plan_id)))
                }
                // if amount is lower name least deposit
                if (this.amount < this.least_deposit) {
                    this.error = 'The minimum deposit is $' + this.least_deposit
                    return
                }
                // calculate earnings with amount and days
                this.error = null
                var total_earnings = 0.00
                for (var plan of selected_plans) {
                    total_earnings += this.calculate_single_plan(plan)
                }
                // add initial deposit to earning
                total_earnings += parseFloat(this.amount)
                
                this.total_earning = Math.round(total_earnings * 100) / 100
                return total_earnings

            }
            return 0.00
        },
        get_plan_by_id(plan_id) {
            for (var plan of this.plans) {
                if (plan.id === plan_id) {
                    return plan
                }
            }
        },
        calculate_single_plan(plan) {
            // calculate earning for one plan
            var plan_total_days = plan.cashout_frequency
            var percent_earning = plan.percent_earning
            var amount = parseFloat(this.amount)
            var days = parseFloat(this.days)
            // calc total earning for complete plan days
            var earning_in_total_days = amount * (percent_earning/100)
            var fraction_diff_in_days = days/plan_total_days
            var earning_in_wanted_days = earning_in_total_days * fraction_diff_in_days
            // should add initial amount to calc in total of plans
            return earning_in_wanted_days
        },
    }
})