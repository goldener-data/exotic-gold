import pytest
from pathlib import Path

from zenodo_client import Zenodo

from any_gold.image.plantseg import PlantSeg
from tests.conftest import TEST_DATASET_LOADING, ZENODO_API_TOKEN


class TestPlantSeg:
    def test_records(self):
        zenodo = Zenodo(access_token=ZENODO_API_TOKEN)
        record_v1 = zenodo.get_latest_record(PlantSeg._VERSIONS[1]["record_id"])
        assert record_v1 == PlantSeg._VERSIONS[1]["record_id"]
        record_v2 = zenodo.get_latest_record(PlantSeg._VERSIONS[2]["record_id"])
        assert record_v2 == PlantSeg._VERSIONS[2]["record_id"]
        record_v3 = zenodo.get_latest_record(PlantSeg._VERSIONS[3]["record_id"])
        assert record_v3 == PlantSeg._VERSIONS[3]["record_id"]

    @pytest.mark.skipif(
        not TEST_DATASET_LOADING, reason="TEST_DATASET_LOADING is not True"
    )
    def test_dataset(self):
        dataset = PlantSeg(
            root=Path("/storage/ml/plantseg"),
            version=3,
            split="train",
        )

        assert len(dataset) == 7916, "Dataset length is not as expected"

        image, mask, plant, disease, index = dataset[0]
        assert index == 0, "Index is not as expected"
        assert image.shape == (1, 3, 853, 640), "Image shape is not as expected"
        assert mask.shape == (1, 1, 853, 640), "Mask shape is not as expected"
        assert dataset.get_image_path(0) == Path(
            "/storage/ml/plantseg/plantsegv3/images/train/apple_mosaic_virus_20.jpg"
        ), "Image path is not as expected"
        assert plant == "Apple"
        assert disease == "apple mosaic virus"
