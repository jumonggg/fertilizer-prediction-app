{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNR/eTqC6dW+rQCmGxW1O66",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/jumonggg/fertilizer-prediction-app/blob/main/app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "source": [
        "# Import necessary libraries\n",
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import joblib\n",
        "\n",
        "# Install the correct scikit-learn version (replace with your version)\n",
        "!pip install scikit-learn==1.2.2 # Changed the version to 1.2.2\n",
        "\n",
        "# Load the trained Random Forest model\n",
        "model = joblib.load('/content/fertilizer_model_rf.pkl')\n",
        "\n",
        "# ... (rest of your code) ..."
      ],
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "0G_dM8ZkOskg",
        "outputId": "afdd25ff-d5b0-407f-d09d-f7c95682f62d"
      },
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: scikit-learn==1.2.2 in /usr/local/lib/python3.11/dist-packages (1.2.2)\n",
            "Requirement already satisfied: numpy>=1.17.3 in /usr/local/lib/python3.11/dist-packages (from scikit-learn==1.2.2) (1.26.4)\n",
            "Requirement already satisfied: scipy>=1.3.2 in /usr/local/lib/python3.11/dist-packages (from scikit-learn==1.2.2) (1.14.1)\n",
            "Requirement already satisfied: joblib>=1.1.1 in /usr/local/lib/python3.11/dist-packages (from scikit-learn==1.2.2) (1.4.2)\n",
            "Requirement already satisfied: threadpoolctl>=2.0.0 in /usr/local/lib/python3.11/dist-packages (from scikit-learn==1.2.2) (3.5.0)\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "/usr/local/lib/python3.11/dist-packages/sklearn/base.py:318: UserWarning: Trying to unpickle estimator DecisionTreeRegressor from version 1.1.3 when using version 1.2.2. This might lead to breaking code or invalid results. Use at your own risk. For more info please refer to:\n",
            "https://scikit-learn.org/stable/model_persistence.html#security-maintainability-limitations\n",
            "  warnings.warn(\n",
            "/usr/local/lib/python3.11/dist-packages/sklearn/base.py:318: UserWarning: Trying to unpickle estimator RandomForestRegressor from version 1.1.3 when using version 1.2.2. This might lead to breaking code or invalid results. Use at your own risk. For more info please refer to:\n",
            "https://scikit-learn.org/stable/model_persistence.html#security-maintainability-limitations\n",
            "  warnings.warn(\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import joblib\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "# Load the trained Random Forest model\n",
        "model = joblib.load('fertilizer_model_rf.pkl')\n",
        "\n",
        "# Streamlit App\n",
        "st.title(\"🌱 Fertilizer Prediction for Farmers\")\n",
        "st.write(\"Upload your CSV file or enter crop and area to predict fertilizer needs.\")\n",
        "\n",
        "# Real-time input fields\n",
        "st.sidebar.header(\"Quick Prediction\")\n",
        "crop = st.sidebar.selectbox(\"Select Crop\", ['Rice', 'Corn', 'Tobacco', 'Peanut', 'Soya', 'Sugarcane'])\n",
        "area = st.sidebar.number_input(\"Enter Area (in hectares)\", min_value=0.1, step=0.01)\n",
        "\n",
        "if st.sidebar.button(\"Predict Fertilizer\"):\n",
        "    # Encode crop type\n",
        "    crop_encoded = pd.factorize([crop])[0][0]\n",
        "    prediction = model.predict([[area, crop_encoded]])[0]\n",
        "    st.sidebar.write(f\"### Predicted Fertilizer: {prediction:.2f} Kg\")\n",
        "\n",
        "# File uploader\n",
        "uploaded_file = st.file_uploader(\"Upload CSV File\", type=[\"csv\"])\n",
        "\n",
        "if uploaded_file is not None:\n",
        "    # Read the uploaded CSV file\n",
        "    data = pd.read_csv(uploaded_file)\n",
        "\n",
        "    # Simple data validation\n",
        "    if 'name' in data.columns and 'crop' in data.columns and 'area' in data.columns:\n",
        "        # Encode crop type\n",
        "        data['crop_encoded'] = pd.factorize(data['crop'])[0]\n",
        "\n",
        "        # Predict fertilizer needs\n",
        "        data['PredictedKg'] = model.predict(data[['area', 'crop_encoded']])\n",
        "\n",
        "        # Show the result\n",
        "        st.write(\"### Predicted Fertilizer Needs\")\n",
        "        st.dataframe(data[['name', 'crop', 'area', 'PredictedKg']])\n",
        "\n",
        "        # Download button\n",
        "        csv = data.to_csv(index=False).encode('utf-8')\n",
        "        st.download_button(\n",
        "            label=\"Download Predictions as CSV\",\n",
        "            data=csv,\n",
        "            file_name='predicted_fertilizer.csv',\n",
        "            mime='text/csv',\n",
        "        )\n",
        "\n",
        "        # Generate summary report\n",
        "        st.write(\"### Fertilizer Summary Report\")\n",
        "        summary = data.groupby('crop')['PredictedKg'].agg(['sum', 'mean']).reset_index()\n",
        "        st.dataframe(summary)\n",
        "\n",
        "        # Plot a bar chart\n",
        "        st.write(\"### Fertilizer Needs per Crop\")\n",
        "        fig, ax = plt.subplots()\n",
        "        ax.bar(summary['crop'], summary['sum'], color='green')\n",
        "        ax.set_xlabel('Crop')\n",
        "        ax.set_ylabel('Total Fertilizer Needed (Kg)')\n",
        "        ax.set_title('Total Fertilizer Requirement per Crop')\n",
        "        st.pyplot(fig)\n",
        "    else:\n",
        "        st.warning(\"Please make sure your CSV file has 'name', 'crop', and 'area' columns.\")\n",
        "\n",
        "st.info(\"This app uses a trained Random Forest model to predict fertilizer requirements. You can either upload a CSV file or use the sidebar input to get predictions.\")\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "DhjIy0PqQYXp",
        "outputId": "6b7d4db2-3e13-4c38-cb5b-35987536b1d1"
      },
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "2025-03-12 03:17:18.613 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.616 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.619 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.620 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.624 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.624 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.625 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.628 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.629 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.631 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.632 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.633 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.636 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.636 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.637 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.638 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.640 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.641 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.642 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.645 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.646 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.647 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.647 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.649 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.650 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.651 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.652 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.652 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.653 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.654 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.655 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-12 03:17:18.656 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
          ]
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "DeltaGenerator()"
            ]
          },
          "metadata": {},
          "execution_count": 7
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# prompt: install sreamlit\n",
        "\n",
        "!pip install streamlit\n",
        "!pip install joblib\n",
        "!pip install pandas\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "DTD4sAP3MoT2",
        "outputId": "3958b885-c2d3-4eaa-dbc4-ffceca36a248"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Collecting streamlit\n",
            "  Downloading streamlit-1.43.2-py2.py3-none-any.whl.metadata (8.9 kB)\n",
            "Requirement already satisfied: altair<6,>=4.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (5.5.0)\n",
            "Requirement already satisfied: blinker<2,>=1.0.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (1.9.0)\n",
            "Requirement already satisfied: cachetools<6,>=4.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (5.5.2)\n",
            "Requirement already satisfied: click<9,>=7.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (8.1.8)\n",
            "Requirement already satisfied: numpy<3,>=1.23 in /usr/local/lib/python3.11/dist-packages (from streamlit) (1.26.4)\n",
            "Requirement already satisfied: packaging<25,>=20 in /usr/local/lib/python3.11/dist-packages (from streamlit) (24.2)\n",
            "Requirement already satisfied: pandas<3,>=1.4.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (2.2.2)\n",
            "Requirement already satisfied: pillow<12,>=7.1.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (11.1.0)\n",
            "Requirement already satisfied: protobuf<6,>=3.20 in /usr/local/lib/python3.11/dist-packages (from streamlit) (4.25.6)\n",
            "Requirement already satisfied: pyarrow>=7.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (18.1.0)\n",
            "Requirement already satisfied: requests<3,>=2.27 in /usr/local/lib/python3.11/dist-packages (from streamlit) (2.32.3)\n",
            "Requirement already satisfied: tenacity<10,>=8.1.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (9.0.0)\n",
            "Requirement already satisfied: toml<2,>=0.10.1 in /usr/local/lib/python3.11/dist-packages (from streamlit) (0.10.2)\n",
            "Requirement already satisfied: typing-extensions<5,>=4.4.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (4.12.2)\n",
            "Collecting watchdog<7,>=2.1.5 (from streamlit)\n",
            "  Downloading watchdog-6.0.0-py3-none-manylinux2014_x86_64.whl.metadata (44 kB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m44.3/44.3 kB\u001b[0m \u001b[31m2.8 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hRequirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /usr/local/lib/python3.11/dist-packages (from streamlit) (3.1.44)\n",
            "Collecting pydeck<1,>=0.8.0b4 (from streamlit)\n",
            "  Downloading pydeck-0.9.1-py2.py3-none-any.whl.metadata (4.1 kB)\n",
            "Requirement already satisfied: tornado<7,>=6.0.3 in /usr/local/lib/python3.11/dist-packages (from streamlit) (6.4.2)\n",
            "Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from altair<6,>=4.0->streamlit) (3.1.6)\n",
            "Requirement already satisfied: jsonschema>=3.0 in /usr/local/lib/python3.11/dist-packages (from altair<6,>=4.0->streamlit) (4.23.0)\n",
            "Requirement already satisfied: narwhals>=1.14.2 in /usr/local/lib/python3.11/dist-packages (from altair<6,>=4.0->streamlit) (1.29.1)\n",
            "Requirement already satisfied: gitdb<5,>=4.0.1 in /usr/local/lib/python3.11/dist-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.12)\n",
            "Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.11/dist-packages (from pandas<3,>=1.4.0->streamlit) (2.8.2)\n",
            "Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.11/dist-packages (from pandas<3,>=1.4.0->streamlit) (2025.1)\n",
            "Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.11/dist-packages (from pandas<3,>=1.4.0->streamlit) (2025.1)\n",
            "Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.27->streamlit) (3.4.1)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.27->streamlit) (3.10)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.27->streamlit) (2.3.0)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.27->streamlit) (2025.1.31)\n",
            "Requirement already satisfied: smmap<6,>=3.0.1 in /usr/local/lib/python3.11/dist-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.2)\n",
            "Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->altair<6,>=4.0->streamlit) (3.0.2)\n",
            "Requirement already satisfied: attrs>=22.2.0 in /usr/local/lib/python3.11/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (25.1.0)\n",
            "Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /usr/local/lib/python3.11/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (2024.10.1)\n",
            "Requirement already satisfied: referencing>=0.28.4 in /usr/local/lib/python3.11/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.36.2)\n",
            "Requirement already satisfied: rpds-py>=0.7.1 in /usr/local/lib/python3.11/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.23.1)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.11/dist-packages (from python-dateutil>=2.8.2->pandas<3,>=1.4.0->streamlit) (1.17.0)\n",
            "Downloading streamlit-1.43.2-py2.py3-none-any.whl (9.7 MB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m9.7/9.7 MB\u001b[0m \u001b[31m71.0 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hDownloading pydeck-0.9.1-py2.py3-none-any.whl (6.9 MB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m6.9/6.9 MB\u001b[0m \u001b[31m86.9 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hDownloading watchdog-6.0.0-py3-none-manylinux2014_x86_64.whl (79 kB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m79.1/79.1 kB\u001b[0m \u001b[31m6.0 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hInstalling collected packages: watchdog, pydeck, streamlit\n",
            "Successfully installed pydeck-0.9.1 streamlit-1.43.2 watchdog-6.0.0\n",
            "Requirement already satisfied: joblib in /usr/local/lib/python3.11/dist-packages (1.4.2)\n",
            "Requirement already satisfied: pandas in /usr/local/lib/python3.11/dist-packages (2.2.2)\n",
            "Requirement already satisfied: numpy>=1.23.2 in /usr/local/lib/python3.11/dist-packages (from pandas) (1.26.4)\n",
            "Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.11/dist-packages (from pandas) (2.8.2)\n",
            "Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.11/dist-packages (from pandas) (2025.1)\n",
            "Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.11/dist-packages (from pandas) (2025.1)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.11/dist-packages (from python-dateutil>=2.8.2->pandas) (1.17.0)\n"
          ]
        }
      ]
    }
  ]
}