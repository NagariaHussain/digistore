<template>
	<div class="my-10 mx-auto max-w-5xl">
		<LoadingSpinner :loading="$resources.getData.loading" />
		<div v-if="data" class="bg-white shadow overflow-hidden sm:rounded-lg">
			<div class="px-4 py-5 sm:px-6">
				<h3 class="text-lg leading-6 font-medium text-gray-900">
					Product Information
				</h3>
				<p class="mt-1 max-w-2xl text-sm text-gray-500">
					Scroll down for download links.
				</p>
			</div>
			<div class="border-t border-gray-200 px-4 py-5 sm:p-0">
				<dl class="sm:divide-y sm:divide-gray-200">
					<div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
						<dt class="text-sm font-medium text-gray-500">Product Id</dt>
						<dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
							{{ productName }}
						</dd>
					</div>
					<div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
						<dt class="text-sm font-medium text-gray-500">Plan</dt>
						<dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
							10$ (PDF + Sticker)
						</dd>
					</div>

					<div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
						<dt class="text-sm font-medium text-gray-500">Attachments</dt>
						<dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
							<ul
								role="list"
								class="
									border border-gray-200
									rounded-md
									divide-y divide-gray-200
								"
							>
								<li
									v-for="asset in data.assets"
									:key="asset.name"
									class="
										pl-3
										pr-4
										py-3
										flex
										items-center
										justify-between
										text-sm
									"
								>
									<div class="w-0 flex-1 flex items-center">
										<PaperClipIcon
											class="flex-shrink-0 h-5 w-5 text-gray-400"
											aria-hidden="true"
										/>
										<span class="ml-2 flex-1 w-0 truncate">
											{{ asset.file }}
										</span>
									</div>
									<div class="ml-4 flex-shrink-0">
										<a
											:href="asset.file"
											target="_blank"
											class="font-medium text-indigo-600 hover:text-indigo-500"
										>
											Download
										</a>
									</div>
								</li>
							</ul>
						</dd>
					</div>
				</dl>
			</div>
		</div>
	</div>
</template>

<script>
import LoadingSpinner from '../components/LoadingSpinner.vue';
import { PaperClipIcon } from '@heroicons/vue/solid';

export default {
	name: 'Purchase',
	components: { LoadingSpinner, PaperClipIcon },
	resources: {
		getData() {
			return {
				method: 'digistore.api.product.get_data',
				params: {
					product: this.productName,
				},
				auto: true,
				onSuccess(d) {
					console.log('Assets', d);
				},
			};
		},
	},
	computed: {
		data() {
			if (!this.$resources.getData.loading && this.$resources.getData.data) {
				return { assets: this.$resources.getData.data };
			}
		},
	},
	props: ['productName'],
};
</script>
