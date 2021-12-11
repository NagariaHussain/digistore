<template>
	<div class="mx-auto max-w-7xl">
		<LoadingSpinner :loading="$resources.productData.loading" />
		<div v-if="$resources.productData.data">
			<div v-if="productData.has_user_purchased" class="px-4 mt-5 max-w-5xl">
				<div class="rounded-md bg-blue-50 p-4">
					<div class="flex">
						<div class="flex-shrink-0">
							<InformationCircleIcon
								class="h-5 w-5 text-blue-400"
								aria-hidden="true"
							/>
						</div>
						<div class="ml-3 flex-1 md:flex md:justify-between">
							<p class="text-sm text-blue-700">
								You have already purchased this product.
							</p>
							<p class="mt-3 text-sm md:mt-0 md:ml-6">
								<router-link
									:to="`/purchases/${productData.has_user_purchased}`"
									v-slot="{ href }"
								>
									<a
										:href="href"
										class="
											whitespace-nowrap
											font-medium
											text-blue-700
											hover:text-blue-600
										"
										>View <span aria-hidden="true">&rarr;</span></a
									>
								</router-link>
							</p>
						</div>
					</div>
				</div>
			</div>
			<div class="mt-8 px-4 prose">
				<h1>
					{{ productData.product_doc.title }}
				</h1>
				<p>{{ productData.product_doc.short_description }}</p>
			</div>

			<div v-if="!productData.has_user_purchased">
				<h2 class="mt-4 px-4 font-bold text-xl">Plans</h2>
				<div class="max-w-7xl pb-24 sm:px-4">
					<div
						class="
							mt-3
							space-y-4
							sm:space-y-0 sm:grid sm:grid-cols-2 sm:gap-6
							lg:max-w-4xl lg:mx-auto
							xl:max-w-none xl:mx-0 xl:grid-cols-4
						"
					>
						<div
							v-for="tier in productData.product_plans"
							:key="tier.title"
							class="
								border border-gray-200
								rounded-lg
								shadow-sm
								divide-y divide-gray-200
							"
						>
							<div class="p-6">
								<h2 class="text-lg leading-6 font-medium text-gray-900">
									{{ tier.title }}
								</h2>
								<p class="mt-4 text-sm text-gray-500">{{ tier.description }}</p>
								<p class="mt-8">
									<span class="text-4xl font-extrabold text-gray-900"
										>${{ tier.price }}</span
									>
								</p>

								<LoadingSpinner :loading="$resources.buyProduct.loading" />
								<button
									v-if="!$resources.buyProduct.loading"
									@click="$resources.buyProduct.submit({ plan: tier.name })"
									class="
										mt-8
										block
										w-full
										bg-gray-800
										border border-gray-800
										rounded-md
										py-2
										text-sm
										font-semibold
										text-white text-center
										hover:bg-gray-900
									"
								>
									Buy {{ tier.title }}
								</button>
							</div>
							<div class="pt-6 pb-8 px-6">
								<h3
									class="
										text-xs
										font-medium
										text-gray-900
										tracking-wide
										uppercase
									"
								>
									What's included
								</h3>
								<ul role="list" class="mt-6 space-y-4">
									<li
										v-for="feature in ['Feature one', 'Feature 2']"
										:key="feature"
										class="flex space-x-3"
									>
										<CheckIcon
											class="flex-shrink-0 h-5 w-5 text-green-500"
											aria-hidden="true"
										/>
										<span class="text-sm text-gray-500">{{ feature }}</span>
									</li>
								</ul>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import LoadingSpinner from '../components/LoadingSpinner.vue';
import { CheckIcon, InformationCircleIcon } from '@heroicons/vue/solid';

export default {
	components: { LoadingSpinner, CheckIcon, InformationCircleIcon },
	name: 'Product',
	props: ['productName'],
	inject: ['$auth'],
	resources: {
		productData() {
			return {
				method: 'digistore.api.product.get',
				params: {
					name: this.productName,
				},
				auto: true,
			};
		},
		buyProduct() {
			return {
				method: 'digistore.api.product.buy',
				validate() {
					if (!this.$auth.isLoggedIn) {
						this.$router.push({ name: 'Login' });
					}
				},
				onSuccess(paymentLink) {
					location.href = paymentLink;
				},
			};
		},
	},
	computed: {
		productData() {
			if (
				!this.$resources.productData.loading &&
				this.$resources.productData.data
			) {
				return this.$resources.productData.data;
			}
		},
	},
};
</script>
