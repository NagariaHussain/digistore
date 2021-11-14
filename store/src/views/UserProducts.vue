<template>
	<div>
		<div class="bg-white px-4 py-5 border-b border-gray-200 sm:px-6">
			<div
				class="
					-ml-4
					-mt-2
					flex
					items-center
					justify-between
					flex-wrap
					sm:flex-nowrap
				"
			>
				<div class="ml-4 mt-2">
					<h3 class="text-lg leading-6 font-medium text-gray-900">
						Your Products
					</h3>
				</div>
				<div class="ml-4 mt-2 flex-shrink-0"></div>
			</div>
		</div>

		<LoadingSpinner :loading="$resources.userProducts.loading" />

		<div v-if="$resources.userProducts.data" class="flow-root mt-6 px-40">
			<ul role="list" class="-my-5 divide-y divide-gray-200">
				<li
					v-for="p in $resources.userProducts.data"
					:key="p.product.name"
					class="py-4"
				>
					<div class="flex items-center space-x-4">
						<div class="flex-shrink-0">
							<img
								class="h-8 w-8 rounded-full"
								:src="p.product.image"
								alt="Product Image"
							/>
						</div>
						<div class="flex-1 min-w-0">
							<p class="text-sm font-medium text-gray-900 truncate">
								{{ p.product.title }}
							</p>
							<p class="text-sm text-gray-500 truncate">
								{{ p.product.category }}
							</p>
						</div>
						<div>
							<router-link :to="`/purchase/${p.product.name}`" v-slot="{ href }">
								<a
									:href="href"
									class="
										inline-flex
										items-center
										shadow-sm
										px-2.5
										py-0.5
										border border-gray-300
										text-sm
										leading-5
										font-medium
										rounded-full
										text-gray-700
										bg-white
										hover:bg-gray-50
									"
								>
									View
								</a>
							</router-link>
						</div>
					</div>
				</li>
			</ul>
		</div>
	</div>
</template>

<script>
import LoadingSpinner from '../components/LoadingSpinner.vue';
export default {
	components: { LoadingSpinner },
	name: 'UserProducts',
	resources: {
		userProducts() {
			console.log(this.$account.user.name);
			return {
				method: 'digistore.api.product.purchased',
				params: {
					user: this.$account.user.name,
				},
				auto: true,
				onSuccess(d) {
					console.log(d);
				},
			};
		},
	},
	inject: ['$auth', '$account'],
};
</script>
