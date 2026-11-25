package esprit.canditature;

import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Candidature {

    public enum Statut {
        EN_ATTENTE,
        ACCEPTEE,
        REFUSEE
    }

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long candidatId;
    private Long jobId;

    @Enumerated(EnumType.STRING)
    private Statut statut;

    protected Candidature() {
    }

    public Candidature(Long candidatId, Long jobId) {
        this.candidatId = candidatId;
        this.jobId = jobId;
        this.statut = Statut.EN_ATTENTE;
    }

    public void modifier(Long candidatId, Long jobId, Statut statut) {
        this.candidatId = candidatId;
        this.jobId = jobId;
        this.statut = statut;
    }

    public Long getId() {
        return id;
    }

    public Long getCandidatId() {
        return candidatId;
    }

    public Long getJobId() {
        return jobId;
    }

    public Statut getStatut() {
        return statut;
    }
}