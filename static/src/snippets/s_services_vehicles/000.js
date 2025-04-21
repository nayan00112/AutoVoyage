/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
// import ajax from 'web.ajax';
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.AutovoyageServiceVehicles = publicWidget.Widget.extend({
    selector: '.s_services_vehicles',

    start: function () {
        console.log('Fetching vehicles...');
        this._fetchVehicles();
        return this._super.apply(this, arguments);
    },

    _fetchVehicles: async function () {
        // Fetch vehicle data from the server
        await rpc('/autovoyage/get_vehicles', {}).then((vehicles) => {
            console.log('Vehicles fetched:', vehicles);
            this._renderVehicles(vehicles);
        }).catch((error) => {
            console.error('Error fetching vehicles:', error);
        });
    },

    _renderVehicles: function (vehicles) {
        const container = this.$el.find('.boxcontainer'); // Find the container for cards
        console.log('------------------------------')

        container.empty(); // Clear any existing content

        vehicles.forEach(vehicle => {
            const cardHtml = `
                <div class="card" style="width: 18rem;">
                <img src="${vehicle.image_url}" class="card-img-top" alt="${vehicle.name}" />
                <div class="card-body">
                        <h5 class="card-title">${vehicle.name}</h5>
                        <p class="card-text mb-1"><strong>Model:</strong> ${vehicle.vehicle_model || 'N/A'}</p>
                        <p class="card-text mb-1"><strong>Service Provider:</strong> ${vehicle.service_provider || 'N/A'}</p>
                        <p class="card-text mb-1"><strong>Fuel Type:</strong> ${vehicle.vehicle_fule_type || 'N/A'}</p>
                        <p class="card-text mb-2"><strong>Rent/Day:</strong> ${vehicle.per_day_cost || 'N/A'}</p>
                        <a href="/autovoyage/book_vehicle/${vehicle.id}" class="btn btn-primary w-100">Book Now</a>
                        </div>
                        </div>
                        `;
            container.append(cardHtml); // Append the card to the container
        });
        console.log(container);
    },
});

export default publicWidget.registry.AutovoyageServiceVehicles;