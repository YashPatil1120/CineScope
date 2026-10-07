import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import ForceGraph2D from "react-force-graph-2d";

import api from "../services/api";
import "./MovieGraph.css";


function MovieGraph({ movieId }) {
    const navigate = useNavigate();
    const graphRef = useRef();

    const [graph, setGraph] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [hoveredNode, setHoveredNode] = useState(null);


    /*
     * Fetch graph data.
     */
    useEffect(() => {
        const fetchGraph = async () => {
            try {
                setLoading(true);
                setError("");

                const response = await api.get(
                    `/api/graph/movie/${movieId}`
                );

                setGraph(response.data);
            } catch (err) {
                console.error(
                    "Failed to load movie graph:",
                    err
                );

                setError(
                    "Unable to load movie relationships."
                );
            } finally {
                setLoading(false);
            }
        };

        if (movieId) {
            fetchGraph();
        }
    }, [movieId]);


    /*
     * Configure force simulation once graph exists.
     */
    useEffect(() => {
        if (!graphRef.current || !graph) {
            return;
        }

        const fg = graphRef.current;

        fg.d3Force("charge").strength(-280);

        fg.d3Force("link").distance((link) => {
            switch (link.relationship) {
                case "HAS_GENRE":
                    return 135;

                case "DIRECTED":
                    return 170;

                case "ACTED_IN":
                    return 165;

                case "RELATED_TO":
                    return 210;

                default:
                    return 160;
            }
        });

        fg.d3Force("center").strength(0.08);

        fg.d3ReheatSimulation();
    }, [graph]);


    /*
     * Node colors.
     */
    const getNodeColor = (node) => {
        switch (node.type) {
            case "movie":
                return "#b18cff";

            case "actor":
                return "#62b0ff";

            case "director":
                return "#ff9b7a";

            case "genre":
                return "#7edc91";

            case "related_movie":
                return "#d19cff";

            default:
                return "#999999";
        }
    };


    /*
     * Node radius.
     */
    const getNodeRadius = (node) => {
        switch (node.type) {
            case "movie":
                return 18;

            case "related_movie":
                return 11;

            case "director":
                return 10;

            case "actor":
                return 8;

            case "genre":
                return 8;

            default:
                return 7;
        }
    };


    /*
     * Human-readable relationship names.
     */
    const getRelationshipLabel = (relationship) => {
        switch (relationship) {
            case "HAS_GENRE":
                return "GENRE";

            case "ACTED_IN":
                return "ACTOR";

            case "DIRECTED":
                return "DIRECTOR";

            case "RELATED_TO":
                return "RELATED";

            default:
                return relationship;
        }
    };


    /*
     * Convert relationship score into a readable percentage.
     *
     * Backend score is currently on a 0-100 style scale.
     */
    const getRelationshipPercentage = (node) => {
        const score = Number(
            node?.metadata?.relationship_score
        );

        if (!Number.isFinite(score)) {
            return null;
        }

        return Math.round(
            Math.max(0, Math.min(100, score))
        );
    };


    /*
     * Relationship strength label.
     */
    const getRelationshipStrength = (score) => {
        if (score === null) {
            return "";
        }

        if (score >= 70) {
            return "Strong match";
        }

        if (score >= 50) {
            return "Good match";
        }

        if (score >= 35) {
            return "Related";
        }

        return "Somewhat related";
    };


    /*
     * Build explanation for intelligent movie relationships.
     */
    const getRelationshipReasons = (node) => {
        if (
            node.type !== "related_movie" ||
            !node.metadata
        ) {
            return [];
        }

        const metadata = node.metadata;
        const reasons = [];

        if (metadata.shared_genres > 0) {
            reasons.push(
                `${metadata.shared_genres} shared ${
                    metadata.shared_genres === 1
                        ? "genre"
                        : "genres"
                }`
            );
        }

        if (metadata.shared_actors > 0) {
            reasons.push(
                `${metadata.shared_actors} shared ${
                    metadata.shared_actors === 1
                        ? "actor"
                        : "actors"
                }`
            );
        }

        if (metadata.same_director) {
            reasons.push("Same director");
        }

        if (
            typeof metadata.semantic_similarity ===
                "number"
        ) {
            reasons.push(
                `${Math.round(
                    metadata.semantic_similarity * 100
                )}% semantic similarity`
            );
        }

        return reasons;
    };


    /*
     * Custom node drawing.
     */
    const paintNode = (node, ctx, globalScale) => {
        const radius = getNodeRadius(node);
        const color = getNodeColor(node);

        const isHovered =
            hoveredNode &&
            hoveredNode.id === node.id;

        const relationshipPercentage =
            getRelationshipPercentage(node);

        const label =
            node.label.length > 22
                ? `${node.label.slice(0, 21)}…`
                : node.label;


        /*
         * Glow around the central movie.
         */
        if (node.type === "movie") {
            ctx.beginPath();

            ctx.arc(
                node.x,
                node.y,
                radius + 10,
                0,
                2 * Math.PI
            );

            ctx.fillStyle =
                "rgba(177, 140, 255, 0.12)";

            ctx.fill();
        }


        /*
         * Hover glow.
         */
        if (isHovered) {
            ctx.beginPath();

            ctx.arc(
                node.x,
                node.y,
                radius + 7,
                0,
                2 * Math.PI
            );

            ctx.fillStyle =
                "rgba(255, 255, 255, 0.10)";

            ctx.fill();
        }


        /*
         * Main node.
         */
        ctx.beginPath();

        ctx.arc(
            node.x,
            node.y,
            radius,
            0,
            2 * Math.PI
        );

        ctx.fillStyle = color;
        ctx.fill();


        /*
         * Main movie gets a white outline.
         */
        if (node.type === "movie") {
            ctx.strokeStyle =
                "rgba(255, 255, 255, 0.85)";

            ctx.lineWidth = 2;

            ctx.stroke();
        }


        /*
         * Related movie gets an outline
         * whose opacity reflects relationship strength.
         */
        if (
            node.type === "related_movie" &&
            relationshipPercentage !== null
        ) {
            const opacity =
                0.35 +
                (relationshipPercentage / 100) *
                    0.45;

            ctx.strokeStyle =
                `rgba(177, 140, 255, ${opacity})`;

            ctx.lineWidth =
                isHovered ? 2.5 : 1.2;

            ctx.stroke();
        }


        /*
         * Only show labels when zoomed enough,
         * hovered, or for the central movie.
         */
        const showLabel =
            globalScale > 0.75 ||
            node.type === "movie" ||
            isHovered;

        if (!showLabel) {
            return;
        }


        const fontSize =
            node.type === "movie"
                ? 13 / globalScale
                : 10 / globalScale;

        ctx.font = `
            ${node.type === "movie" ? "700" : "500"}
            ${fontSize}px
            Inter, Arial, sans-serif
        `;

        ctx.textAlign = "center";
        ctx.textBaseline = "top";

        ctx.fillStyle =
            isHovered || node.type === "movie"
                ? "#ffffff"
                : "#c7c7d0";

        ctx.fillText(
            label,
            node.x,
            node.y + radius + 6 / globalScale
        );


        /*
         * Show relationship percentage
         * underneath related movie names.
         */
        if (
            node.type === "related_movie" &&
            relationshipPercentage !== null
        ) {
            const scoreFontSize =
                8 / globalScale;

            ctx.font = `
                700
                ${scoreFontSize}px
                Inter, Arial, sans-serif
            `;

            ctx.fillStyle =
                isHovered
                    ? "#e6d9ff"
                    : "#a994cf";

            ctx.fillText(
                `${relationshipPercentage}% related`,
                node.x,
                node.y +
                    radius +
                    18 / globalScale
            );
        }
    };


    /*
     * Custom relationship labels.
     */
    const paintLinkLabel = (
        link,
        ctx,
        globalScale
    ) => {
        const start = link.source;
        const end = link.target;

        if (
            typeof start !== "object" ||
            typeof end !== "object"
        ) {
            return;
        }

        const label = getRelationshipLabel(
            link.relationship
        );

        const x =
            (start.x + end.x) / 2;

        const y =
            (start.y + end.y) / 2;

        const fontSize =
            8 / globalScale;

        ctx.font = `
            600
            ${fontSize}px
            Inter, Arial, sans-serif
        `;

        ctx.textAlign = "center";
        ctx.textBaseline = "middle";


        /*
         * Make RELATED labels more visible.
         */
        const labelColor =
            link.relationship === "RELATED_TO"
                ? "#bca5e8"
                : "#74747f";


        /*
         * Small dark background behind label.
         */
        const textWidth =
            ctx.measureText(label).width;

        ctx.fillStyle =
            "rgba(8, 8, 11, 0.82)";

        ctx.fillRect(
            x - textWidth / 2 - 4 / globalScale,
            y - 5 / globalScale,
            textWidth + 8 / globalScale,
            10 / globalScale
        );

        ctx.fillStyle = labelColor;

        ctx.fillText(
            label,
            x,
            y
        );
    };


    /*
     * Click behavior.
     */
    const handleNodeClick = (node) => {
        /*
         * Related movie → Movie Details.
         */
        if (
            node.type === "related_movie" &&
            node.metadata?.movie_id
        ) {
            navigate(
                `/movies/${node.metadata.movie_id}`
            );

            return;
        }

        /*
         * Clicking the main movie does nothing.
         */
    };


    /*
     * Loading state.
     */
    if (loading) {
        return (
            <div className="movie-graph-state">
                <div className="graph-spinner"></div>

                <span>
                    Building movie relationships...
                </span>
            </div>
        );
    }


    /*
     * Error state.
     */
    if (error) {
        return (
            <div className="movie-graph-state movie-graph-error">
                {error}
            </div>
        );
    }


    /*
     * Empty graph.
     */
    if (
        !graph ||
        graph.nodes.length === 0
    ) {
        return (
            <div className="movie-graph-state">
                No relationship data available.
            </div>
        );
    }


    /*
     * Hovered related movie information.
     */
    const hoveredReasons =
        hoveredNode?.type === "related_movie"
            ? getRelationshipReasons(hoveredNode)
            : [];

    const hoveredPercentage =
        getRelationshipPercentage(
            hoveredNode
        );

    const hoveredStrength =
        getRelationshipStrength(
            hoveredPercentage
        );


    return (
        <div className="movie-graph">

            {/* Header */}
            <div className="movie-graph-header">

                <div>
                    <span className="graph-kicker">
                        CINESCOPE KNOWLEDGE GRAPH
                    </span>

                    <h2>
                        Explore {graph.movie_title}
                    </h2>

                    <p>
                        Explore the people, genres and
                        movies connected to this film.
                        Relationships are ranked using
                        semantic similarity and movie metadata.
                    </p>
                </div>

                <div className="graph-stats">

                    <div className="graph-stat">
                        <strong>
                            {graph.nodes.length}
                        </strong>

                        <span>
                            Nodes
                        </span>
                    </div>

                    <div className="graph-stat">
                        <strong>
                            {graph.links.length}
                        </strong>

                        <span>
                            Connections
                        </span>
                    </div>

                </div>

            </div>


            {/* Legend */}
            <div className="graph-legend">

                <div className="legend-item">
                    <span
                        className="legend-dot legend-movie"
                    ></span>

                    Movie
                </div>

                <div className="legend-item">
                    <span
                        className="legend-dot legend-actor"
                    ></span>

                    Actor
                </div>

                <div className="legend-item">
                    <span
                        className="legend-dot legend-director"
                    ></span>

                    Director
                </div>

                <div className="legend-item">
                    <span
                        className="legend-dot legend-genre"
                    ></span>

                    Genre
                </div>

                <div className="legend-item">
                    <span
                        className="legend-dot legend-related"
                    ></span>

                    Related Movie
                </div>

            </div>


            {/* Intelligent relationship information */}
            {hoveredNode?.type === "related_movie" && (
                <div className="graph-relationship-card">

                    <div className="relationship-card-main">

                        <div>
                            <span className="relationship-card-kicker">
                                INTELLIGENT MATCH
                            </span>

                            <h3>
                                {hoveredNode.label}
                            </h3>

                            <span className="relationship-strength">
                                {hoveredStrength}
                            </span>
                        </div>

                        {hoveredPercentage !== null && (
                            <div className="relationship-score">
                                <strong>
                                    {hoveredPercentage}%
                                </strong>

                                <span>
                                    related
                                </span>
                            </div>
                        )}

                    </div>


                    {hoveredReasons.length > 0 && (
                        <div className="relationship-reasons">

                            {hoveredReasons.map(
                                (reason, index) => (
                                    <span
                                        key={`${reason}-${index}`}
                                        className="relationship-reason"
                                    >
                                        {reason}
                                    </span>
                                )
                            )}

                        </div>
                    )}

                </div>
            )}


            {/* Graph */}
            <div className="movie-graph-canvas">

                <ForceGraph2D
                    ref={graphRef}

                    graphData={{
                        nodes: graph.nodes,
                        links: graph.links,
                    }}

                    backgroundColor="#09090d"

                    nodeCanvasObject={
                        paintNode
                    }

                    nodePointerAreaPaint={(
                        node,
                        color,
                        ctx
                    ) => {
                        ctx.fillStyle = color;

                        ctx.beginPath();

                        ctx.arc(
                            node.x,
                            node.y,
                            getNodeRadius(node) + 7,
                            0,
                            2 * Math.PI
                        );

                        ctx.fill();
                    }}

                    linkColor={(link) => {
                        if (
                            link.relationship ===
                            "RELATED_TO"
                        ) {
                            const score =
                                Number(
                                    link.metadata?.score
                                );

                            if (
                                Number.isFinite(score)
                            ) {
                                const opacity =
                                    0.15 +
                                    Math.min(
                                        score / 100,
                                        1
                                    ) *
                                        0.45;

                                return `rgba(
                                    177,
                                    140,
                                    255,
                                    ${opacity}
                                )`;
                            }

                            return "rgba(177, 140, 255, 0.25)";
                        }

                        return "rgba(145, 145, 160, 0.18)";
                    }}

                    linkWidth={(link) => {
                        if (
                            link.relationship ===
                            "RELATED_TO"
                        ) {
                            const score =
                                Number(
                                    link.metadata?.score
                                );

                            if (
                                Number.isFinite(score)
                            ) {
                                return (
                                    1 +
                                    Math.min(
                                        score / 100,
                                        1
                                    ) * 2
                                );
                            }

                            return 1.2;
                        }

                        return 1.4;
                    }}

                    linkDirectionalArrowLength={4}

                    linkDirectionalArrowRelPos={1}

                    linkCanvasObjectMode={() =>
                        "after"
                    }

                    linkCanvasObject={
                        paintLinkLabel
                    }

                    onNodeHover={(node) => {
                        setHoveredNode(
                            node || null
                        );
                    }}

                    onNodeClick={
                        handleNodeClick
                    }

                    nodeLabel={(node) => {
                        if (
                            node.type === "actor"
                        ) {
                            return `${node.label}${
                                node.metadata
                                    ?.character
                                    ? ` as ${node.metadata.character}`
                                    : ""
                            }`;
                        }

                        if (
                            node.type ===
                            "related_movie"
                        ) {
                            const score =
                                getRelationshipPercentage(
                                    node
                                );

                            return score !== null
                                ? `${node.label} • ${score}% related`
                                : node.label;
                        }

                        return node.label;
                    }}

                    cooldownTicks={120}

                    warmupTicks={50}

                    enableNodeDrag={true}

                    enableZoomInteraction={true}

                    enablePanInteraction={true}

                    d3VelocityDecay={0.35}

                    d3AlphaDecay={0.025}
                />

            </div>


            {/* Footer hint */}
            <div className="graph-footer">

                <span>
                    Drag nodes to explore
                </span>

                <span className="graph-footer-separator">
                    •
                </span>

                <span>
                    Scroll to zoom
                </span>

                <span className="graph-footer-separator">
                    •
                </span>

                <span>
                    Hover related movies to see why they match
                </span>

                <span className="graph-footer-separator">
                    •
                </span>

                <span>
                    Click a related movie to open it
                </span>

            </div>

        </div>
    );
}


export default MovieGraph;