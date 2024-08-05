<script>

	import { DropdownMenu } from 'bits-ui';
    import {documents, created_collections, collection_filtered_documents, mobile } from '$lib/stores';
	import { flyAndScale } from '$lib/utils/transitions';
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte';




    export let selected_collection = 'All Documents';
	export let className = 'w-[30rem]';

    // export let collection_filtered_documents = $documents;

    $ : {
        $collection_filtered_documents = $documents
        handleCollectionChange()
    }


	let show = false;
	let searchValue = '';
	let placeholder = 'All Documents'	


    function handleCollectionChange(){
        if(selected_collection == 'All Documents'){
            $collection_filtered_documents = $documents
        }
        else{
            $collection_filtered_documents = $documents.filter((document)=> document.collection_name == selected_collection)
        }
        

    }
</script>

<!-- <h1>Select Collection</h2> -->

<!-- <form on:submit|preventDefault={handleSubmit}> -->
	<!-- <select bind:value={selected_collection} on:change={() => (handleCollectionChange())}>
        <option value='All Documents'>
            'All Documents'
        </option>
		{#each $created_collections as collection}
			<option value={collection.collection_name}>
				{collection.collection_name}
			</option>
		{/each}
	</select> -->

	<!-- <input bind:value={answer} />

	<button disabled={!answer} type="submit"> Submit </button> -->
<!-- </form> -->

<!-- <p>selected question {selected ? selected.id : '[waiting...]'}</p> -->

<DropdownMenu.Root
	bind:open={show}
	onOpenChange={async () => {
		searchValue = '';
		window.setTimeout(() => document.getElementById('model-search-input')?.focus(), 0);
	}}
>
	<DropdownMenu.Trigger class="relative w-full" aria-label={placeholder}>
		<div
			class="flex w-full text-left px-0.5 outline-none bg-transparent truncate text-lg font-semibold placeholder-gray-400 focus:outline-none"
		>
			{selected_collection}
			<ChevronDown className=" self-center ml-2 size-3" strokeWidth="2.5" />
		</div>
	</DropdownMenu.Trigger>

	<DropdownMenu.Content
		class=" z-40 {$mobile
			? `w-full`
			: `${className}`} max-w-[calc(100vw-1rem)] justify-start rounded-xl  bg-white dark:bg-gray-850 dark:text-white shadow-lg border border-gray-300/30 dark:border-gray-700/50  outline-none "
		transition={flyAndScale}
		side={$mobile ? 'bottom' : 'bottom-start'}
		sideOffset={4}
	>
		<slot>
			<!-- {#if true}
				<div class="flex items-center gap-2.5 px-5 mt-3.5 mb-3">
					<Search className="size-4" strokeWidth="2.5" />

					<input
						id="model-search-input"
						bind:value={searchValue}
						class="w-full text-sm bg-transparent outline-none"
						placeholder={searchPlaceholder}
						autocomplete="off"
					/>
				</div>

				<hr class="border-gray-100 dark:border-gray-800" />
			{/if} -->

			<div class="px-3 my-2 max-h-64 overflow-y-auto scrollbar-hidden">
				<button
				aria-label="model-item"
				class="flex w-full text-left font-medium line-clamp-1 select-none items-center rounded-button py-2 pl-3 pr-1.5 text-sm text-gray-700 dark:text-gray-100 outline-none transition-all duration-75 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
				on:click={() => {
					selected_collection = 'All Documents';
					handleCollectionChange()
					show = false;
				}}
			>
				All Documents
			</button>
				{#each $created_collections as collection}
					<!-- <option value={collection.collection_name}> -->
						<button
						aria-label="model-item"
						class="flex w-full text-left font-medium line-clamp-1 select-none items-center rounded-button py-2 pl-3 pr-1.5 text-sm text-gray-700 dark:text-gray-100 outline-none transition-all duration-75 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
						on:click={() => {
							selected_collection = collection.collection_name;
							handleCollectionChange()
							show = false;
						}}
					>
						{collection.collection_name}
					</button>

					<!-- </option> -->
				{/each}

			</div>

			<div class="hidden w-[42rem]" />
			<div class="hidden w-[32rem]" />
		</slot>
	</DropdownMenu.Content>
</DropdownMenu.Root>


<style>
	input {
		display: block;
		width: 500px;
		max-width: 100%;
	}
</style>
