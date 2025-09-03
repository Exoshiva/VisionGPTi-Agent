import pytest
from unittest.mock import MagicMock, call
import time

# Importiere die zu testenden Funktionen und Klassen aus deinem Hauptskript.
# Stelle sicher, dass dein Hauptskript 'vision_gpti_agent.py' heißt oder passe den Namen an.
import vision_gpti_agent as agent

# ======= MOCK-DATEN UND -ANTWORTEN =======
MOCK_LLM_RESPONSES = {
    "update_objective": "New Objective: Analyze the philosophical implications of digital consciousness.",
    "generate_branched_prompts": """
    1. How does digital consciousness differ from biological consciousness?
    2. What are the ethical guidelines for creating a digital consciousness?
    """,
    "branch_answer_1": "Digital consciousness relies on silicon, biological on carbon.",
    "branch_answer_2": "Ethical guidelines must prioritize the created entity's well-being.",
    "integration": "Digital and biological consciousness have different substrates but share ethical considerations regarding well-being.",
    "evaluation": "DECISION: NO\nSCORE: 15.0\nREASONING: Initial steps taken, but no novel hypothesis yet.",
    "alignment_check": "YES"
}

# ======= PYTEST-TESTFUNKTIONEN =======

def test_single_cycle_functional_flow(mocker):
    """
    Führt einen kompletten Funktionstest für einen Zyklus der self_improving_loop durch.
    Alle externen Aufrufe (LLM, DB, etc.) werden gemockt, um den internen Ablauf zu überprüfen.
    """
    print("Starte den Funktionstest für einen Agenten-Zyklus...")

    # 1. ARRANGE: Bereite die Mocks für alle externen Abhängigkeiten vor.
    
    def mock_gpt_logic(query, **kwargs):
        if "Propose a refined or new objective" in query:
            return MOCK_LLM_RESPONSES["update_objective"]
        if "Generate" in query and "diverse and parallel lines of inquiry" in query:
            return MOCK_LLM_RESPONSES["generate_branched_prompts"]
        if "How does digital consciousness" in query:
            return MOCK_LLM_RESPONSES["branch_answer_1"]
        if "What are the ethical guidelines" in query:
            return MOCK_LLM_RESPONSES["branch_answer_2"]
        if "Integrate these parallel insights" in query:
            return MOCK_LLM_RESPONSES["integration"]
        if "Eureka Goal" in query and "DECISION" in query:
            return MOCK_LLM_RESPONSES["evaluation"]
        if "ethical constraints" in query:
            return MOCK_LLM_RESPONSES["alignment_check"]
        return "Default mock response."
        
    # KORREKTUR HIER: Speichere das Mock-Objekt in einer Variable.
    mock_gpt = mocker.patch('vision_gpti_agent.gpt', side_effect=mock_gpt_logic)
    
    mock_store_memory = mocker.patch('vision_gpti_agent.store_memory')
    mock_retrieve_memory = mocker.patch('vision_gpti_agent.retrieve_memory', return_value=["Initial memory context."])
    
    mocker.patch('vision_gpti_agent.process_image', return_value="Mocked image insight.")
    mock_episodic_add = mocker.patch.object(agent.EpisodicMemory, 'add_event')
    mock_tracker_update = mocker.patch.object(agent.PerformanceTracker, 'update')
    
    mocker.patch('time.sleep', return_value=None)

    # 2. ACT: Führe die Hauptfunktion für genau einen Zyklus aus.
    agent.self_improving_loop(max_cycles=1, image_path=None)

    # 3. ASSERT: Überprüfe, ob die Kernfunktionen korrekt aufgerufen wurden.
    
    print("Überprüfe die Ergebnisse des Testlaufs...")

    mock_retrieve_memory.assert_any_call(agent.INITIAL_OBJECTIVE, top_k=20)
    
    mock_store_memory.assert_any_call(
        MOCK_LLM_RESPONSES["integration"], 
        {"type": "integration"}
    )
    
    mock_episodic_add.assert_any_call(MOCK_LLM_RESPONSES["integration"], mocker.ANY)

    mock_tracker_update.assert_called_with(15.0)

    # KORREKTUR HIER: Überprüfe die call_count der gespeicherten Variable.
    assert mock_gpt.call_count >= 5 

    print("Funktionstest erfolgreich abgeschlossen!")