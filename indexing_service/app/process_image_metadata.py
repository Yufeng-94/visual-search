METADATA_ITEM_KEYS = [
    'scale', 
    'viewpoint', 
    'zoom_in', 
    'style', 
    'bounding_box', 
    'occlusion', 
    'category_id',
]

def extract_useful_metadata(raw_metadata: dict) -> dict:
    metadata = {}
    # Prepare extracted metadata
    metadata['segmented'] = False
    for k, v in raw_metadata.items():
        if 'item' in k:
            item_metadata = {}
            for i_k in METADATA_ITEM_KEYS:
                item_metadata[i_k] = v.get(i_k, None)
            metadata[k] = item_metadata
        else:
            metadata[k] = v
    return metadata