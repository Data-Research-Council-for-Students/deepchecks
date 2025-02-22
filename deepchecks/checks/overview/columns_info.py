# ----------------------------------------------------------------------------
# Copyright (C) 2021 Deepchecks (https://www.deepchecks.com)
#
# This file is part of Deepchecks.
# Deepchecks is distributed under the terms of the GNU Affero General
# Public License (version 3 or later).
# You should have received a copy of the GNU Affero General Public License
# along with Deepchecks.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------
#
"""Module contains columns_info check."""
import typing as t
import pandas as pd
from deepchecks import CheckResult
from deepchecks.base import Dataset
from deepchecks.base.check import SingleDatasetBaseCheck
from deepchecks.utils.features import N_TOP_MESSAGE, calculate_feature_importance_or_none, \
                                      column_importance_sorter_dict


__all__ = ['ColumnsInfo']


class ColumnsInfo(SingleDatasetBaseCheck):
    """Return the role and logical type of each column.

    Args:
        n_top_columns (int): (optional - used only if model was specified)
                             amount of columns to show ordered by feature importance (date, index, label are first)
    """

    def __init__(self, n_top_columns: int = 10):
        super().__init__()
        self.n_top_columns = n_top_columns

    def run(
      self,
      dataset: t.Union[Dataset, pd.DataFrame],
      model=None
    ) -> CheckResult:
        """Run check.

        Args:
          dataset (Union[Dataset, pandas.DataFrame]): any dataset.

        Returns:
          CheckResult: value is dictionary of a column and its role and logical type.
          display a table of the dictionary.
        """
        dataset = Dataset.validate_dataset_or_dataframe(dataset)
        feature_importances = calculate_feature_importance_or_none(model, dataset)
        return self._columns_info(dataset, feature_importances)

    def _columns_info(self, dataset: Dataset, feature_importances: pd.Series = None):
        value = dataset.columns_info
        value = column_importance_sorter_dict(value, dataset, feature_importances, self.n_top_columns)
        df = pd.DataFrame.from_dict(value, orient='index', columns=['role'])
        df = df.transpose()

        return CheckResult(value, header='Columns Info', display=[N_TOP_MESSAGE % self.n_top_columns, df])
